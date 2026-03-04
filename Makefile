CC ?= gcc
CFLAGS = -O3 -march=native -Wall -Wextra -std=c11 -g
LDFLAGS = -lz
SANITIZE_FLAGS = -fsanitize=address,undefined -fno-omit-frame-pointer

# Source files
SRC_DIR = src
INCLUDE_DIR = include
BENCH_DIR = bench
TEST_DIR = tests

# Main decompressor sources
NAIVE_SRCS = $(SRC_DIR)/naive_inflate.c
FAST_SRCS = $(SRC_DIR)/fast_inflate.c $(SRC_DIR)/fast_decode.c $(SRC_DIR)/bitreader.c \
            $(SRC_DIR)/table_build.c $(SRC_DIR)/simd_literals.c

# Third-party libraries (built from source)
THIRD_PARTY = third_party
ZLIB_NG_DIR = $(THIRD_PARTY)/zlib-ng
LIBDEFLATE_DIR = $(THIRD_PARTY)/libdeflate

# Targets
.PHONY: all clean test bench naive fast deps hello

all: hello naive

hello: $(SRC_DIR)/hello.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

naive: $(SRC_DIR)/naive_inflate.c $(INCLUDE_DIR)/fast_deflate.h
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -o test_naive $(SRC_DIR)/naive_inflate.c $(TEST_DIR)/test_correctness.c $(LDFLAGS)

bench_harness: $(BENCH_DIR)/benchmark.c $(SRC_DIR)/naive_inflate.c $(INCLUDE_DIR)/fast_deflate.h
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -I$(LIBDEFLATE_DIR) \
		-o $@ $< $(SRC_DIR)/naive_inflate.c \
		$(LIBDEFLATE_DIR)/libdeflate.a \
		$(LDFLAGS) -lm -ldl

test_correctness: $(TEST_DIR)/test_correctness.c $(SRC_DIR)/naive_inflate.c $(INCLUDE_DIR)/fast_deflate.h
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -o $@ $< $(SRC_DIR)/naive_inflate.c $(LDFLAGS)

test_correctness_asan: $(TEST_DIR)/test_correctness.c $(SRC_DIR)/naive_inflate.c $(INCLUDE_DIR)/fast_deflate.h
	$(CC) $(CFLAGS) $(SANITIZE_FLAGS) -I$(INCLUDE_DIR) -o $@ $< $(SRC_DIR)/naive_inflate.c $(LDFLAGS)

clean:
	rm -f hello test_naive test_correctness test_correctness_asan bench_harness
	rm -f *.o

deps:
	@echo "Building third-party dependencies..."
	@mkdir -p $(THIRD_PARTY)
	@if [ ! -d "$(ZLIB_NG_DIR)" ]; then \
		git clone --depth 1 https://github.com/zlib-ng/zlib-ng.git $(ZLIB_NG_DIR); \
	fi
	@if [ ! -d "$(LIBDEFLATE_DIR)" ]; then \
		git clone --depth 1 https://github.com/ebiggers/libdeflate.git $(LIBDEFLATE_DIR); \
	fi
