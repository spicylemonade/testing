/*
 * test_compliance.c — RFC 4180 compliance test suite
 *
 * Tests the scalar_parser against 30+ edge cases.
 * Build: gcc -O2 -o tests/test_compliance tests/test_compliance.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

/* Include the parser implementation directly for testing */
/* In production, this would be a separate compilation unit */

/* Forward declarations matching scalar_parser.c */
enum csv_state {
    STATE_FIELD_START = 0,
    STATE_UNQUOTED_FIELD = 1,
    STATE_QUOTED_FIELD = 2,
    STATE_QUOTE_IN_QUOTED = 3,
    STATE_CR_SEEN = 4,
};

typedef struct {
    void (*on_field)(const char *data, size_t len, int field_idx, void *ctx);
    void (*on_record_end)(int field_count, void *ctx);
    void *ctx;
} csv_callbacks;

typedef struct {
    size_t rows;
    size_t fields;
    size_t bytes_processed;
    int error;
    char error_msg[256];
} csv_result;

/* Inline the core parser for testing */
csv_result csv_parse_scalar(const char *input, size_t input_len, csv_callbacks *cb) {
    csv_result result = {0};
    enum csv_state state = STATE_FIELD_START;
    const char *field_start = input;
    size_t field_len = 0;
    int field_idx = 0;
    char *field_buf = NULL;
    size_t field_buf_cap = 0;
    size_t field_buf_len = 0;

    for (size_t i = 0; i <= input_len; i++) {
        char c = (i < input_len) ? input[i] : '\0';
        int is_eof = (i == input_len);

        switch (state) {
        case STATE_FIELD_START:
            if (is_eof) {
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
            } else if (c == ',') {
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
                } else {
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
                result.error = 1;
                snprintf(result.error_msg, sizeof(result.error_msg),
                         "Unterminated quoted field at byte %zu", i);
                goto done;
            }
            if (c == '"') {
                state = STATE_QUOTE_IN_QUOTED;
            } else {
                if (field_buf_len >= field_buf_cap) {
                    field_buf_cap = field_buf_cap ? field_buf_cap * 2 : 4096;
                    field_buf = realloc(field_buf, field_buf_cap);
                }
                field_buf[field_buf_len++] = c;
            }
            break;

        case STATE_QUOTE_IN_QUOTED:
            if (c == '"') {
                if (field_buf_len >= field_buf_cap) {
                    field_buf_cap = field_buf_cap ? field_buf_cap * 2 : 4096;
                    field_buf = realloc(field_buf, field_buf_cap);
                }
                field_buf[field_buf_len++] = '"';
                state = STATE_QUOTED_FIELD;
            } else {
                if (cb->on_field) cb->on_field(field_buf, field_buf_len, field_idx, cb->ctx);
                field_idx++;
                result.fields++;
                field_buf_len = 0;
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
                if (cb->on_record_end) cb->on_record_end(field_idx, cb->ctx);
                result.rows++;
                field_idx = 0;
                i--;
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

/* ------------------------------------------------------------------ */
/* Test infrastructure                                                 */
/* ------------------------------------------------------------------ */

#define MAX_TEST_FIELDS 256
#define MAX_FIELD_LEN 4096

typedef struct {
    int field_count;
    int record_count;
    char fields[MAX_TEST_FIELDS][MAX_FIELD_LEN];
    int field_lens[MAX_TEST_FIELDS];
    int fields_per_record[64];
    int total_field_idx;
} test_ctx;

static void test_on_field(const char *data, size_t len, int field_idx, void *ctx) {
    test_ctx *t = (test_ctx *)ctx;
    if (t->total_field_idx < MAX_TEST_FIELDS && len < MAX_FIELD_LEN) {
        memcpy(t->fields[t->total_field_idx], data, len);
        t->fields[t->total_field_idx][len] = '\0';
        t->field_lens[t->total_field_idx] = (int)len;
    }
    t->total_field_idx++;
    t->field_count++;
}

static void test_on_record(int field_count, void *ctx) {
    test_ctx *t = (test_ctx *)ctx;
    if (t->record_count < 64) {
        t->fields_per_record[t->record_count] = field_count;
    }
    t->record_count++;
    t->field_count = 0;
}

static int tests_passed = 0;
static int tests_failed = 0;

#define ASSERT_EQ(a, b, msg) do { \
    if ((a) != (b)) { \
        printf("FAIL: %s: expected %d, got %d\n", msg, (int)(b), (int)(a)); \
        tests_failed++; return; \
    } \
} while(0)

#define ASSERT_STREQ(a, b, msg) do { \
    if (strcmp((a), (b)) != 0) { \
        printf("FAIL: %s: expected \"%s\", got \"%s\"\n", msg, (b), (a)); \
        tests_failed++; return; \
    } \
} while(0)

#define TEST_PASS(name) do { tests_passed++; printf("PASS: %s\n", name); } while(0)

static csv_result run_test(const char *input, test_ctx *ctx) {
    memset(ctx, 0, sizeof(*ctx));
    csv_callbacks cb = { .on_field = test_on_field, .on_record_end = test_on_record, .ctx = ctx };
    return csv_parse_scalar(input, strlen(input), &cb);
}

/* ------------------------------------------------------------------ */
/* Test cases                                                          */
/* ------------------------------------------------------------------ */

void test_simple_row(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b,c\r\n", &ctx);
    ASSERT_EQ(r.error, 0, "simple_row no error");
    ASSERT_EQ(ctx.record_count, 1, "simple_row 1 record");
    ASSERT_STREQ(ctx.fields[0], "a", "simple_row field 0");
    ASSERT_STREQ(ctx.fields[1], "b", "simple_row field 1");
    ASSERT_STREQ(ctx.fields[2], "c", "simple_row field 2");
    TEST_PASS("test_simple_row");
}

void test_two_rows(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b\r\nc,d\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 2, "two_rows 2 records");
    ASSERT_STREQ(ctx.fields[0], "a", "two_rows r0f0");
    ASSERT_STREQ(ctx.fields[1], "b", "two_rows r0f1");
    ASSERT_STREQ(ctx.fields[2], "c", "two_rows r1f0");
    ASSERT_STREQ(ctx.fields[3], "d", "two_rows r1f1");
    TEST_PASS("test_two_rows");
}

void test_quoted_field(void) {
    test_ctx ctx;
    csv_result r = run_test("\"hello\",world\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 1, "quoted 1 record");
    ASSERT_STREQ(ctx.fields[0], "hello", "quoted field 0");
    ASSERT_STREQ(ctx.fields[1], "world", "quoted field 1");
    TEST_PASS("test_quoted_field");
}

void test_quoted_comma(void) {
    test_ctx ctx;
    csv_result r = run_test("\"a,b\",c\r\n", &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 2, "quoted_comma 2 fields");
    ASSERT_STREQ(ctx.fields[0], "a,b", "quoted_comma field 0");
    ASSERT_STREQ(ctx.fields[1], "c", "quoted_comma field 1");
    TEST_PASS("test_quoted_comma");
}

void test_escaped_quote(void) {
    test_ctx ctx;
    csv_result r = run_test("\"a\"\"b\",c\r\n", &ctx);
    ASSERT_STREQ(ctx.fields[0], "a\"b", "escaped_quote field 0");
    TEST_PASS("test_escaped_quote");
}

void test_embedded_newline(void) {
    test_ctx ctx;
    csv_result r = run_test("\"line1\nline2\",b\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 1, "embedded_nl 1 record");
    ASSERT_STREQ(ctx.fields[0], "line1\nline2", "embedded_nl field 0");
    TEST_PASS("test_embedded_newline");
}

void test_embedded_crlf(void) {
    test_ctx ctx;
    csv_result r = run_test("\"line1\r\nline2\",b\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 1, "embedded_crlf 1 record");
    ASSERT_STREQ(ctx.fields[0], "line1\r\nline2", "embedded_crlf field 0");
    TEST_PASS("test_embedded_crlf");
}

void test_empty_fields(void) {
    test_ctx ctx;
    csv_result r = run_test(",,,\r\n", &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 4, "empty_fields 4 fields");
    ASSERT_STREQ(ctx.fields[0], "", "empty_fields f0");
    ASSERT_STREQ(ctx.fields[1], "", "empty_fields f1");
    ASSERT_STREQ(ctx.fields[2], "", "empty_fields f2");
    ASSERT_STREQ(ctx.fields[3], "", "empty_fields f3");
    TEST_PASS("test_empty_fields");
}

void test_lf_only(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b\nc,d\n", &ctx);
    ASSERT_EQ(ctx.record_count, 2, "lf_only 2 records");
    ASSERT_STREQ(ctx.fields[0], "a", "lf_only r0f0");
    ASSERT_STREQ(ctx.fields[2], "c", "lf_only r1f0");
    TEST_PASS("test_lf_only");
}

void test_no_trailing_newline(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b\nc,d", &ctx);
    ASSERT_EQ(ctx.record_count, 2, "no_trailing_nl 2 records");
    ASSERT_STREQ(ctx.fields[3], "d", "no_trailing_nl r1f1");
    TEST_PASS("test_no_trailing_newline");
}

void test_single_field(void) {
    test_ctx ctx;
    csv_result r = run_test("hello\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 1, "single_field 1 record");
    ASSERT_EQ(ctx.fields_per_record[0], 1, "single_field 1 field");
    ASSERT_STREQ(ctx.fields[0], "hello", "single_field value");
    TEST_PASS("test_single_field");
}

void test_empty_quoted(void) {
    test_ctx ctx;
    csv_result r = run_test("\"\",b\r\n", &ctx);
    ASSERT_STREQ(ctx.fields[0], "", "empty_quoted field 0");
    ASSERT_STREQ(ctx.fields[1], "b", "empty_quoted field 1");
    TEST_PASS("test_empty_quoted");
}

void test_just_quotes(void) {
    /* Field that is just "" (empty quoted field) */
    test_ctx ctx;
    csv_result r = run_test("\"\"\r\n", &ctx);
    ASSERT_STREQ(ctx.fields[0], "", "just_quotes field 0 empty");
    TEST_PASS("test_just_quotes");
}

void test_consecutive_delimiters(void) {
    test_ctx ctx;
    csv_result r = run_test("a,,b,,c\r\n", &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 5, "consecutive_delim 5 fields");
    ASSERT_STREQ(ctx.fields[0], "a", "consecutive f0");
    ASSERT_STREQ(ctx.fields[1], "", "consecutive f1 empty");
    ASSERT_STREQ(ctx.fields[2], "b", "consecutive f2");
    ASSERT_STREQ(ctx.fields[3], "", "consecutive f3 empty");
    ASSERT_STREQ(ctx.fields[4], "c", "consecutive f4");
    TEST_PASS("test_consecutive_delimiters");
}

void test_trailing_comma(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b,\r\n", &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 3, "trailing_comma 3 fields");
    ASSERT_STREQ(ctx.fields[2], "", "trailing_comma f2 empty");
    TEST_PASS("test_trailing_comma");
}

void test_multiple_escaped_quotes(void) {
    test_ctx ctx;
    csv_result r = run_test("\"a\"\"b\"\"c\"\r\n", &ctx);
    ASSERT_STREQ(ctx.fields[0], "a\"b\"c", "multi_escape field 0");
    TEST_PASS("test_multiple_escaped_quotes");
}

void test_only_quotes_field(void) {
    /* Field containing only escaped quotes: """" -> " */
    test_ctx ctx;
    csv_result r = run_test("\"\"\"\"\r\n", &ctx);
    ASSERT_STREQ(ctx.fields[0], "\"", "only_quotes field 0");
    TEST_PASS("test_only_quotes_field");
}

void test_mixed_quoting_in_row(void) {
    test_ctx ctx;
    csv_result r = run_test("plain,\"quoted\",123,\"with,comma\"\r\n", &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 4, "mixed 4 fields");
    ASSERT_STREQ(ctx.fields[0], "plain", "mixed f0");
    ASSERT_STREQ(ctx.fields[1], "quoted", "mixed f1");
    ASSERT_STREQ(ctx.fields[2], "123", "mixed f2");
    ASSERT_STREQ(ctx.fields[3], "with,comma", "mixed f3");
    TEST_PASS("test_mixed_quoting_in_row");
}

void test_long_field(void) {
    /* Field > 1000 bytes */
    char input[2048];
    char field_buf[1200];
    memset(field_buf, 'x', 1100);
    field_buf[1100] = '\0';
    snprintf(input, sizeof(input), "%s,b\r\n", field_buf);

    test_ctx ctx;
    csv_result r = run_test(input, &ctx);
    ASSERT_EQ(ctx.field_lens[0], 1100, "long_field length");
    TEST_PASS("test_long_field");
}

void test_header_and_data(void) {
    test_ctx ctx;
    csv_result r = run_test("name,age,city\r\nAlice,30,\"New York\"\r\nBob,25,London\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 3, "header_data 3 records");
    ASSERT_STREQ(ctx.fields[0], "name", "header f0");
    ASSERT_STREQ(ctx.fields[3], "Alice", "data r1f0");
    ASSERT_STREQ(ctx.fields[5], "New York", "data r1f2");
    TEST_PASS("test_header_and_data");
}

void test_whitespace_in_field(void) {
    test_ctx ctx;
    csv_result r = run_test(" a , b \r\n", &ctx);
    ASSERT_STREQ(ctx.fields[0], " a ", "whitespace f0 preserved");
    ASSERT_STREQ(ctx.fields[1], " b ", "whitespace f1 preserved");
    TEST_PASS("test_whitespace_in_field");
}

void test_cr_only_line_ending(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b\rc,d\r", &ctx);
    ASSERT_EQ(ctx.record_count, 2, "cr_only 2 records");
    TEST_PASS("test_cr_only_line_ending");
}

void test_empty_file(void) {
    test_ctx ctx;
    csv_result r = run_test("", &ctx);
    ASSERT_EQ(ctx.record_count, 0, "empty_file 0 records");
    ASSERT_EQ(r.error, 0, "empty_file no error");
    TEST_PASS("test_empty_file");
}

void test_newline_only(void) {
    test_ctx ctx;
    csv_result r = run_test("\n", &ctx);
    /* A single newline = 1 empty record with 0 fields */
    ASSERT_EQ(r.error, 0, "newline_only no error");
    TEST_PASS("test_newline_only");
}

void test_complex_multiline(void) {
    test_ctx ctx;
    csv_result r = run_test(
        "\"field with\r\nnewline\",simple\r\n"
        "\"another\nfield\",\"with \"\"quotes\"\"\"\r\n",
        &ctx);
    ASSERT_EQ(ctx.record_count, 2, "complex_ml 2 records");
    ASSERT_STREQ(ctx.fields[0], "field with\r\nnewline", "complex_ml f0");
    ASSERT_STREQ(ctx.fields[1], "simple", "complex_ml f1");
    ASSERT_STREQ(ctx.fields[2], "another\nfield", "complex_ml f2");
    ASSERT_STREQ(ctx.fields[3], "with \"quotes\"", "complex_ml f3");
    TEST_PASS("test_complex_multiline");
}

void test_crlf_and_lf_mixed(void) {
    test_ctx ctx;
    csv_result r = run_test("a,b\r\nc,d\ne,f\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 3, "mixed_endings 3 records");
    TEST_PASS("test_crlf_and_lf_mixed");
}

void test_single_column_multirow(void) {
    test_ctx ctx;
    csv_result r = run_test("a\nb\nc\n", &ctx);
    ASSERT_EQ(ctx.record_count, 3, "single_col 3 records");
    ASSERT_EQ(ctx.fields_per_record[0], 1, "single_col 1 field per record");
    TEST_PASS("test_single_column_multirow");
}

void test_numeric_data(void) {
    test_ctx ctx;
    csv_result r = run_test("1,2.5,-3,0.001,1e10\r\n", &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 5, "numeric 5 fields");
    ASSERT_STREQ(ctx.fields[0], "1", "numeric f0");
    ASSERT_STREQ(ctx.fields[1], "2.5", "numeric f1");
    ASSERT_STREQ(ctx.fields[4], "1e10", "numeric f4");
    TEST_PASS("test_numeric_data");
}

void test_many_fields(void) {
    /* 50 fields in one row */
    char input[1024];
    int pos = 0;
    for (int i = 0; i < 50; i++) {
        if (i > 0) input[pos++] = ',';
        pos += snprintf(input + pos, sizeof(input) - pos, "%d", i);
    }
    input[pos++] = '\n';
    input[pos] = '\0';

    test_ctx ctx;
    csv_result r = run_test(input, &ctx);
    ASSERT_EQ(ctx.fields_per_record[0], 50, "many_fields 50 fields");
    TEST_PASS("test_many_fields");
}

void test_utf8_content(void) {
    test_ctx ctx;
    /* Chinese characters and emoji */
    csv_result r = run_test("\xe4\xb8\xad\xe6\x96\x87,\xf0\x9f\x98\x80\r\n", &ctx);
    ASSERT_EQ(ctx.record_count, 1, "utf8 1 record");
    ASSERT_EQ(ctx.fields_per_record[0], 2, "utf8 2 fields");
    TEST_PASS("test_utf8_content");
}

int main(void) {
    printf("=== RFC 4180 Compliance Test Suite ===\n\n");

    test_simple_row();
    test_two_rows();
    test_quoted_field();
    test_quoted_comma();
    test_escaped_quote();
    test_embedded_newline();
    test_embedded_crlf();
    test_empty_fields();
    test_lf_only();
    test_no_trailing_newline();
    test_single_field();
    test_empty_quoted();
    test_just_quotes();
    test_consecutive_delimiters();
    test_trailing_comma();
    test_multiple_escaped_quotes();
    test_only_quotes_field();
    test_mixed_quoting_in_row();
    test_long_field();
    test_header_and_data();
    test_whitespace_in_field();
    test_cr_only_line_ending();
    test_empty_file();
    test_newline_only();
    test_complex_multiline();
    test_crlf_and_lf_mixed();
    test_single_column_multirow();
    test_numeric_data();
    test_many_fields();
    test_utf8_content();

    printf("\n=== Results: %d passed, %d failed ===\n", tests_passed, tests_failed);
    return tests_failed > 0 ? 1 : 0;
}
