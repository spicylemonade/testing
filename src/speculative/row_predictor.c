/*
 * row_predictor.c — Speculative row-length prediction for CSV parsing
 *
 * Implements an EWMA (Exponentially Weighted Moving Average) predictor
 * for row byte-lengths and field counts, enabling pre-allocation of
 * output buffers.
 *
 * Build:
 *   gcc -O2 -o row_predictor row_predictor.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

/* EWMA predictor for row properties */
typedef struct {
    double predicted_row_bytes;
    double predicted_field_count;
    double alpha;            /* smoothing factor (0.1 = slow adapt, 0.5 = fast) */
    size_t n_samples;
    size_t n_correct_bytes;   /* predictions within 20% of actual */
    size_t n_correct_fields;  /* predictions with exact field count */
    size_t n_total;
    size_t alloc_calls_with;  /* allocation calls with prediction */
    size_t alloc_calls_without; /* allocation calls without (naive) */
} row_predictor;

static void predictor_init(row_predictor *p, double alpha) {
    memset(p, 0, sizeof(*p));
    p->alpha = alpha;
    p->predicted_row_bytes = 100;  /* initial guess */
    p->predicted_field_count = 10; /* initial guess */
}

static void predictor_update(row_predictor *p, double actual_bytes, double actual_fields) {
    p->n_total++;

    /* Check prediction accuracy */
    if (p->n_samples > 0) {
        double byte_error = fabs(actual_bytes - p->predicted_row_bytes) / (actual_bytes + 1);
        if (byte_error < 0.20) p->n_correct_bytes++;
        if ((int)actual_fields == (int)(p->predicted_field_count + 0.5)) p->n_correct_fields++;
    }

    /* Update EWMA */
    if (p->n_samples == 0) {
        p->predicted_row_bytes = actual_bytes;
        p->predicted_field_count = actual_fields;
    } else {
        p->predicted_row_bytes = p->alpha * actual_bytes + (1 - p->alpha) * p->predicted_row_bytes;
        p->predicted_field_count = p->alpha * actual_fields + (1 - p->alpha) * p->predicted_field_count;
    }
    p->n_samples++;
}

/*
 * Simulate speculative allocation:
 * - With prediction: allocate predicted_row_bytes; realloc only if actual > predicted
 * - Without prediction: allocate per-field (malloc for each field)
 */
static void predictor_count_allocs(row_predictor *p, double actual_bytes, double actual_fields) {
    /* With prediction: 1 allocation per row (pre-sized), realloc only on misprediction */
    p->alloc_calls_with++;
    if (actual_bytes > p->predicted_row_bytes * 1.2) {
        p->alloc_calls_with++;  /* extra realloc for misprediction */
    }

    /* Without prediction: 1 malloc per field */
    p->alloc_calls_without += (size_t)actual_fields;
}

/*
 * Test the predictor on a real CSV file.
 */
static void test_predictor(const char *input, size_t input_len, double alpha, const char *label) {
    row_predictor pred;
    predictor_init(&pred, alpha);

    size_t pos = 0;
    int in_quotes = 0;
    size_t row_start = 0;
    int field_count = 1;  /* starts at 1 for the first field */

    while (pos < input_len) {
        char c = input[pos];
        if (c == '"') {
            in_quotes = !in_quotes;
        } else if (!in_quotes) {
            if (c == ',') {
                field_count++;
            } else if (c == '\n') {
                size_t row_bytes = pos - row_start;
                /* Remove CR if present */
                if (row_bytes > 0 && pos > 0 && input[pos - 1] == '\r') {
                    row_bytes--;
                }

                predictor_count_allocs(&pred, (double)row_bytes, (double)field_count);
                predictor_update(&pred, (double)row_bytes, (double)field_count);

                row_start = pos + 1;
                field_count = 1;
            }
        }
        pos++;
    }

    /* Handle last row without trailing newline */
    if (row_start < input_len) {
        size_t row_bytes = input_len - row_start;
        predictor_count_allocs(&pred, (double)row_bytes, (double)field_count);
        predictor_update(&pred, (double)row_bytes, (double)field_count);
    }

    double byte_accuracy = pred.n_total > 0 ? 100.0 * pred.n_correct_bytes / pred.n_total : 0;
    double field_accuracy = pred.n_total > 0 ? 100.0 * pred.n_correct_fields / pred.n_total : 0;
    double alloc_reduction = pred.alloc_calls_without > 0
        ? (double)pred.alloc_calls_without / pred.alloc_calls_with : 0;

    printf("{\"dataset\":\"%s\",\"alpha\":%.2f,"
           "\"total_rows\":%zu,"
           "\"byte_prediction_accuracy_pct\":%.2f,"
           "\"field_prediction_accuracy_pct\":%.2f,"
           "\"predicted_row_bytes\":%.1f,"
           "\"predicted_field_count\":%.1f,"
           "\"alloc_calls_with_prediction\":%zu,"
           "\"alloc_calls_without_prediction\":%zu,"
           "\"alloc_reduction_factor\":%.1f}\n",
           label, alpha, pred.n_total,
           byte_accuracy, field_accuracy,
           pred.predicted_row_bytes, pred.predicted_field_count,
           pred.alloc_calls_with, pred.alloc_calls_without,
           alloc_reduction);
}

static char *mmap_file(const char *path, size_t *out_size) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) { perror("open"); return NULL; }
    struct stat st;
    if (fstat(fd, &st) < 0) { perror("fstat"); close(fd); return NULL; }
    *out_size = (size_t)st.st_size;
    if (*out_size == 0) { close(fd); return (char *)calloc(1, 1); }
    char *data = mmap(NULL, *out_size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);
    if (data == MAP_FAILED) { perror("mmap"); return NULL; }
    return data;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <csvfile> [alpha=0.1]\n", argv[0]);
        return 1;
    }

    double alpha = 0.1;
    if (argc >= 3) alpha = atof(argv[2]);

    size_t file_size;
    char *data = mmap_file(argv[1], &file_size);
    if (!data) return 1;

    /* Extract just the filename for the label */
    const char *label = strrchr(argv[1], '/');
    label = label ? label + 1 : argv[1];

    test_predictor(data, file_size, alpha, label);

    if (file_size > 0) munmap(data, file_size);
    return 0;
}
