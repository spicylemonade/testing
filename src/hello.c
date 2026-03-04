/*
 * hello.c - Trivial build test for the fast DEFLATE project.
 * Verifies that zlib is available and the build system works.
 */

#include <stdio.h>
#include <string.h>
#include <zlib.h>

int main(void) {
    const char *msg = "Hello from fast-deflate project!";
    unsigned char compressed[256];
    unsigned char decompressed[256];
    uLongf comp_len = sizeof(compressed);
    uLongf decomp_len = sizeof(decompressed);

    /* Compress with zlib */
    int rc = compress(compressed, &comp_len, (const Bytef *)msg, strlen(msg) + 1);
    if (rc != Z_OK) {
        fprintf(stderr, "compress() failed: %d\n", rc);
        return 1;
    }

    /* Decompress with zlib */
    rc = uncompress(decompressed, &decomp_len, compressed, comp_len);
    if (rc != Z_OK) {
        fprintf(stderr, "uncompress() failed: %d\n", rc);
        return 1;
    }

    printf("zlib version: %s\n", zlibVersion());
    printf("Original:     %s\n", msg);
    printf("Decompressed: %s\n", decompressed);
    printf("Compressed:   %lu -> %lu bytes\n", (unsigned long)strlen(msg) + 1, (unsigned long)comp_len);

    if (strcmp((char *)decompressed, msg) == 0) {
        printf("SUCCESS: Build system works, zlib linked correctly.\n");
        return 0;
    } else {
        fprintf(stderr, "FAILURE: Decompressed data does not match original.\n");
        return 1;
    }
}
