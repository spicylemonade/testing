/*
 * scalar_parser.c — RFC 4180 compliant scalar CSV parser (baseline)
 *
 * State-machine parser that processes one byte at a time.
 * This serves as the correctness reference and performance baseline
 * against which the SIMD parser will be compared.
 *
 * Usage:
 *   ./scalar_parser <csvfile> [--benchmark] [--count-only] [--validate]
 *
 * Build:
 *   gcc -O2 -o scalar_parser scalar_parser.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

/* Parser states */
enum csv_state {
    STATE_FIELD_START = 0,
    STATE_UNQUOTED_FIELD = 1,
    STATE_QUOTED_FIELD = 2,
    STATE_QUOTE_IN_QUOTED = 3,
    STATE_CR_SEEN = 4,
};

/* Callback interface */
typedef struct {
    void (*on_field)(const char *data, size_t len, int field_idx, void *ctx);
    void (*on_record_end)(int field_count, void *ctx);
    void *ctx;
} csv_callbacks;

/* Parser result */
typedef struct {
    size_t rows;
    size_t fields;
    size_t bytes_processed;
    int error;
    char error_msg[256];
} csv_result;

/* Count-only context */
typedef struct {
    size_t total_rows;
    size_t total_fields;
    size_t max_field_len;
    size_t total_field_bytes;
} count_ctx;

static void count_on_field(const char *data, size_t len, int field_idx, void *ctx) {
    count_ctx *c = (count_ctx *)ctx;
    c->total_fields++;
    c->total_field_bytes += len;
    if (len > c->max_field_len) c->max_field_len = len;
}

static void count_on_record(int field_count, void *ctx) {
    count_ctx *c = (count_ctx *)ctx;
    c->total_rows++;
}

/*
 * Core scalar CSV parser.
 * Processes the input byte-by-byte through a state machine.
 */
csv_result csv_parse_scalar(const char *input, size_t input_len, csv_callbacks *cb) {
    csv_result result = {0};
    enum csv_state state = STATE_FIELD_START;
    const char *field_start = input;
    size_t field_len = 0;
    int field_idx = 0;
    int in_quoted = 0;

    /* Temporary buffer for unescaping quoted fields */
    char *field_buf = NULL;
    size_t field_buf_cap = 0;
    size_t field_buf_len = 0;

    for (size_t i = 0; i <= input_len; i++) {
        char c = (i < input_len) ? input[i] : '\0';
        int is_eof = (i == input_len);

        switch (state) {
        case STATE_FIELD_START:
            if (is_eof) {
                /* At EOF in FIELD_START: only emit a record if we have
                   accumulated fields (i.e., there was a trailing comma).
                   A trailing newline should NOT produce an extra record. */
                if (field_idx > 0) {
                    if (cb->on_field) cb->on_field("", 0, field_idx, cb->ctx);
                    field_idx++;
                    if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                    result.rows++;
                }
                goto done;
            }
            field_start = input + i;
            field_len = 0;
            field_buf_len = 0;
            if (c == '"') {
                state = STATE_QUOTED_FIELD;
                in_quoted = 1;
            } else if (c == ',') {
                /* Empty field */
                if (cb->on_field) cb->on_field("", 0, field_idx, cb->ctx);
                field_idx++;
                result.fields++;
                state = STATE_FIELD_START;
            } else if (c == '\r') {
                if (field_idx > 0) {
                    if (cb->on_field) cb->on_field("", 0, field_idx, cb->ctx);
                    field_idx++;
                    result.fields++;
                }
                state = STATE_CR_SEEN;
            } else if (c == '\n') {
                if (field_idx > 0) {
                    if (cb->on_field) cb->on_field("", 0, field_idx, cb->ctx);
                    field_idx++;
                    result.fields++;
                }
                if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                result.rows++;
                field_idx = 0;
                state = STATE_FIELD_START;
            } else {
                field_start = input + i;
                field_len = 1;
                state = STATE_UNQUOTED_FIELD;
            }
            break;

        case STATE_UNQUOTED_FIELD:
            if (is_eof || c == ',' || c == '\r' || c == '\n') {
                if (cb->on_field) cb->on_field(field_start, field_len, field_idx, cb->ctx);
                field_idx++;
                result.fields++;
                if (is_eof) {
                    if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                    result.rows++;
                    goto done;
                } else if (c == ',') {
                    state = STATE_FIELD_START;
                } else if (c == '\r') {
                    state = STATE_CR_SEEN;
                } else { /* \n */
                    if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                    result.rows++;
                    field_idx = 0;
                    state = STATE_FIELD_START;
                }
            } else {
                field_len++;
            }
            break;

        case STATE_QUOTED_FIELD:
            if (is_eof) {
                /* Unterminated quoted field */
                result.error = 1;
                snprintf(result.error_msg, sizeof(result.error_msg),
                         "Unterminated quoted field at byte %zu", i);
                goto done;
            }
            if (c == '"') {
                state = STATE_QUOTE_IN_QUOTED;
            } else {
                /* Accumulate into field buffer for proper unescaping */
                if (field_buf_len >= field_buf_cap) {
                    field_buf_cap = field_buf_cap ? field_buf_cap * 2 : 4096;
                    field_buf = realloc(field_buf, field_buf_cap);
                }
                field_buf[field_buf_len++] = c;
            }
            break;

        case STATE_QUOTE_IN_QUOTED:
            if (c == '"') {
                /* Escaped quote ("") */
                if (field_buf_len >= field_buf_cap) {
                    field_buf_cap = field_buf_cap ? field_buf_cap * 2 : 4096;
                    field_buf = realloc(field_buf, field_buf_cap);
                }
                field_buf[field_buf_len++] = '"';
                state = STATE_QUOTED_FIELD;
            } else {
                /* End of quoted field */
                if (cb->on_field) cb->on_field(field_buf, field_buf_len, field_idx, cb->ctx);
                field_idx++;
                result.fields++;
                field_buf_len = 0;
                in_quoted = 0;

                if (is_eof) {
                    if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                    result.rows++;
                    goto done;
                } else if (c == ',') {
                    state = STATE_FIELD_START;
                } else if (c == '\r') {
                    state = STATE_CR_SEEN;
                } else if (c == '\n') {
                    if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                    result.rows++;
                    field_idx = 0;
                    state = STATE_FIELD_START;
                } else {
                    /* Character after closing quote that isn't comma/newline */
                    /* Lenient: treat as content of next unquoted region */
                    field_start = input + i;
                    field_len = 1;
                    state = STATE_UNQUOTED_FIELD;
                }
            }
            break;

        case STATE_CR_SEEN:
            if (c == '\n' || is_eof) {
                if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                result.rows++;
                field_idx = 0;
                state = STATE_FIELD_START;
                if (is_eof) goto done;
            } else {
                /* CR without LF — treat CR as line ending, reprocess this byte */
                if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                result.rows++;
                field_idx = 0;
                i--; /* reprocess current byte */
                state = STATE_FIELD_START;
            }
            break;
        }
    }

done:
    result.bytes_processed = input_len;
    free(field_buf);
    return result;
}

/*
 * Memory-map a file and return pointer + size.
 */
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

static void munmap_file(char *data, size_t size) {
    if (data && size > 0) munmap(data, size);
}

/* High-resolution timer */
static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <csvfile> [--benchmark] [--count-only] [--validate]\n", argv[0]);
        return 1;
    }

    const char *filepath = argv[1];
    int benchmark = 0, count_only = 0, validate = 0;
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--benchmark") == 0) benchmark = 1;
        if (strcmp(argv[i], "--count-only") == 0) count_only = 1;
        if (strcmp(argv[i], "--validate") == 0) validate = 1;
    }

    size_t file_size;
    char *data = mmap_file(filepath, &file_size);
    if (!data) return 1;

    count_ctx ctx = {0};
    csv_callbacks cb = {
        .on_field = count_on_field,
        .on_record_end = count_on_record,
        .ctx = &ctx,
    };

    int n_runs = benchmark ? 5 : 1;
    double best_time = 1e30;
    csv_result result = {0};

    for (int run = 0; run < n_runs; run++) {
        memset(&ctx, 0, sizeof(ctx));
        double t0 = now_sec();
        result = csv_parse_scalar(data, file_size, &cb);
        double elapsed = now_sec() - t0;
        if (elapsed < best_time) best_time = elapsed;
    }

    if (result.error) {
        fprintf(stderr, "Parse error: %s\n", result.error_msg);
        munmap_file(data, file_size);
        return 1;
    }

    double mb = file_size / (1024.0 * 1024.0);
    double throughput_mbs = mb / best_time;
    double rows_per_sec = ctx.total_rows / best_time;

    if (benchmark) {
        printf("{\"parser\":\"scalar_baseline\",\"file\":\"%s\","
               "\"file_size_bytes\":%zu,\"rows\":%zu,\"fields\":%zu,"
               "\"best_time_sec\":%.6f,\"throughput_mb_per_sec\":%.2f,"
               "\"rows_per_sec\":%.0f,\"max_field_len\":%zu,"
               "\"avg_field_bytes\":%.1f}\n",
               filepath, file_size, ctx.total_rows, ctx.total_fields,
               best_time, throughput_mbs, rows_per_sec,
               ctx.max_field_len,
               ctx.total_fields > 0 ? (double)ctx.total_field_bytes / ctx.total_fields : 0);
    } else {
        printf("File: %s\n", filepath);
        printf("Size: %.2f MB\n", mb);
        printf("Rows: %zu\n", ctx.total_rows);
        printf("Fields: %zu\n", ctx.total_fields);
        printf("Max field length: %zu\n", ctx.max_field_len);
        printf("Time: %.4f sec\n", best_time);
        printf("Throughput: %.2f MB/s\n", throughput_mbs);
        printf("Rows/sec: %.0f\n", rows_per_sec);
    }

    munmap_file(data, file_size);
    return 0;
}
