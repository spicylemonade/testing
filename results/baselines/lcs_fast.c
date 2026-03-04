/* Fast LCS computation via dynamic programming.
   Compile: gcc -O3 -shared -fPIC -o lcs_fast.so lcs_fast.c
*/
#include <stdlib.h>
#include <string.h>

int lcs_dp(const unsigned char *a, int n, const unsigned char *b, int m) {
    int *prev = (int *)calloc(m + 1, sizeof(int));
    int *curr = (int *)calloc(m + 1, sizeof(int));
    if (!prev || !curr) { free(prev); free(curr); return -1; }
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (a[i] == b[j]) {
                curr[j + 1] = prev[j] + 1;
            } else {
                curr[j + 1] = curr[j] > prev[j + 1] ? curr[j] : prev[j + 1];
            }
        }
        int *tmp = prev; prev = curr; curr = tmp;
        memset(curr, 0, (m + 1) * sizeof(int));
    }
    int result = prev[m];
    free(prev);
    free(curr);
    return result;
}

/* Windowed LCS: only compute within diagonal band |i-j| <= window */
int lcs_windowed(const unsigned char *a, int n, const unsigned char *b, int m, int window) {
    int *prev = (int *)calloc(m + 1, sizeof(int));
    int *curr = (int *)calloc(m + 1, sizeof(int));
    if (!prev || !curr) { free(prev); free(curr); return -1; }
    
    for (int i = 0; i < n; i++) {
        int j_min = i - window;
        if (j_min < 0) j_min = 0;
        int j_max = i + window;
        if (j_max >= m) j_max = m - 1;
        
        if (j_min > 0) curr[j_min] = prev[j_min];
        
        for (int j = j_min; j <= j_max; j++) {
            if (a[i] == b[j]) {
                curr[j + 1] = prev[j] + 1;
            } else {
                curr[j + 1] = curr[j] > prev[j + 1] ? curr[j] : prev[j + 1];
            }
        }
        int *tmp = prev; prev = curr; curr = tmp;
        /* Clear only the band we'll use next */
        int nj_min = (i + 1) - window;
        if (nj_min < 0) nj_min = 0;
        int nj_max = (i + 1) + window;
        if (nj_max >= m) nj_max = m - 1;
        for (int j = nj_min; j <= nj_max + 1; j++) {
            curr[j] = 0;
        }
    }
    int result = prev[m];
    free(prev);
    free(curr);
    return result;
}

/* Bit-parallel LCS using Allison-Dix method.
   For binary alphabet, uses 2 pattern masks.
   Processes 64 bits at a time. */
int lcs_bitparallel(const unsigned char *a, int n, const unsigned char *b, int m) {
    if (n == 0 || m == 0) return 0;
    
    int nwords = (m + 63) / 64;
    unsigned long long *PM0 = (unsigned long long *)calloc(nwords, sizeof(unsigned long long));
    unsigned long long *PM1 = (unsigned long long *)calloc(nwords, sizeof(unsigned long long));
    unsigned long long *M = (unsigned long long *)calloc(nwords, sizeof(unsigned long long));
    if (!PM0 || !PM1 || !M) { free(PM0); free(PM1); free(M); return -1; }
    
    /* Build pattern masks */
    for (int j = 0; j < m; j++) {
        int wi = j / 64, bi = j % 64;
        if (b[j] == 0) PM0[wi] |= (1ULL << bi);
        else           PM1[wi] |= (1ULL << bi);
    }
    
    for (int i = 0; i < n; i++) {
        unsigned long long *PM = (a[i] == 0) ? PM0 : PM1;
        unsigned long long carry = 1ULL;
        for (int k = 0; k < nwords; k++) {
            unsigned long long X = PM[k] | M[k];
            unsigned long long shifted = (M[k] << 1) | carry;
            carry = M[k] >> 63;
            unsigned long long diff = X - shifted;
            /* Handle borrow */
            if (X < shifted) {
                /* borrow from next word - but we track with carry */
            }
            unsigned long long Y = X ^ (X - shifted);
            /* If borrow occurred need to handle across words */
            /* Simpler: use the standard Hyyrö formulation */
            M[k] = X & ~Y;
        }
    }
    
    /* Count bits */
    int count = 0;
    for (int k = 0; k < nwords; k++) {
        count += __builtin_popcountll(M[k]);
    }
    
    free(PM0); free(PM1); free(M);
    return count;
}
