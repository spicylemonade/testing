cmake_minimum_required(VERSION 3.16)
project(simd_base64 C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Compiler flags
add_compile_options(-Wall -Wextra -Wpedantic -O3)

# Detect architecture
if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|AMD64|amd64")
    set(ARCH_X86_64 TRUE)
    message(STATUS "Target: x86-64")
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64|arm64|ARM64")
    set(ARCH_ARM64 TRUE)
    message(STATUS "Target: ARM64")
else()
    message(STATUS "Target: ${CMAKE_SYSTEM_PROCESSOR} (scalar only)")
endif()

# Scalar library (always built)
add_library(base64_scalar STATIC src/scalar/base64_scalar.c)
target_include_directories(base64_scalar PUBLIC src/common)

# Test for scalar decoder
add_executable(test_scalar tests/test_scalar.c)
target_link_libraries(test_scalar base64_scalar)
target_include_directories(test_scalar PRIVATE src/common)

# Benchmark framework (Phase 2)
# add_executable(bench_base64 benchmarks/bench_main.c)
# target_link_libraries(bench_base64 base64_scalar)

enable_testing()
add_test(NAME test_scalar COMMAND test_scalar)
