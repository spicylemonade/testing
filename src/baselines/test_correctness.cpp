// Correctness test suite for all GCD baseline implementations
// Compile: g++ -O3 -march=native -std=c++20 -o test_correctness test_correctness.cpp
#include "gcd_baselines.h"
#include <iostream>
#include <random>
#include <cassert>
#include <numeric>
#include <functional>
#include <string>
#include <vector>
#include <chrono>

using namespace gcd_baseline;

// Reference GCD (trusted)
template <typename T>
T ref_gcd(T a, T b) {
    while (b) { T t = b; b = a % b; a = t; }
    return a;
}

static int tests_passed = 0;
static int tests_failed = 0;

template <typename T>
void check(const char* name, T a, T b, T expected, T got) {
    if (got != expected) {
        tests_failed++;
        if (tests_failed <= 20) {
            std::cerr << "FAIL " << name << ": gcd(" << (uint64_t)a << ", " << (uint64_t)b 
                      << ") = " << (uint64_t)expected << " but got " << (uint64_t)got << "\n";
        }
    } else {
        tests_passed++;
    }
}

template <typename T>
void test_single(const char* name, T (*fn)(T, T), T a, T b) {
    T expected = ref_gcd(a, b);
    T got = fn(a, b);
    check(name, a, b, expected, got);
}

template <typename T>
void test_all_impls(T a, T b) {
    test_single("euclid", gcd_euclid<T>, a, b);
    test_single("stein_classic", gcd_stein_classic<T>, a, b);
    test_single("binary_ctz", gcd_binary_ctz<T>, a, b);
    test_single("binary_opt", gcd_binary_opt<T>, a, b);
}

template <typename T>
void run_test_suite(const char* type_name) {
    std::cout << "Testing " << type_name << " (" << sizeof(T)*8 << "-bit)...\n";
    
    // Edge cases
    test_all_impls<T>(0, 0);
    test_all_impls<T>(0, 1);
    test_all_impls<T>(1, 0);
    test_all_impls<T>(1, 1);
    test_all_impls<T>(0, 42);
    test_all_impls<T>(42, 0);
    
    // Coprime
    test_all_impls<T>(13, 7);
    test_all_impls<T>(17, 31);
    test_all_impls<T>(97, 89);
    
    // Equal
    test_all_impls<T>(42, 42);
    test_all_impls<T>(1000, 1000);
    
    // Powers of 2
    test_all_impls<T>(1, 2);
    test_all_impls<T>(2, 4);
    test_all_impls<T>(8, 16);
    test_all_impls<T>(64, 256);
    test_all_impls<T>(T(1) << 20, T(1) << 30);
    
    // One divides the other
    test_all_impls<T>(6, 12);
    test_all_impls<T>(100, 1000);
    
    // Fibonacci (worst case for Euclid)
    T fib_a = 1, fib_b = 1;
    for (int i = 0; i < 40 && fib_b < (T(1) << (sizeof(T)*8 - 2)); i++) {
        test_all_impls<T>(fib_a, fib_b);
        T t = fib_a + fib_b;
        fib_a = fib_b;
        fib_b = t;
    }
    
    // Max values
    if constexpr (sizeof(T) <= 8) {
        T maxval = ~T(0);
        test_all_impls<T>(maxval, maxval);
        test_all_impls<T>(maxval, 1);
        test_all_impls<T>(maxval, maxval - 1);
        test_all_impls<T>(maxval, 2);
    }
    
    // Random pairs: 10,000+
    std::mt19937_64 rng(42);
    for (int i = 0; i < 12000; i++) {
        T a, b;
        if constexpr (sizeof(T) <= 8) {
            a = rng();
            b = rng();
        } else {
            a = (static_cast<unsigned __int128>(rng()) << 64) | rng();
            b = (static_cast<unsigned __int128>(rng()) << 64) | rng();
        }
        // Various distributions
        if (i < 3000) {
            // uniform random
        } else if (i < 6000) {
            // skewed: one much larger
            b = b & 0xFFFF;
        } else if (i < 9000) {
            // nearly equal
            b = a + (rng() & 0xFF);
        } else {
            // one is small
            a = rng() & 0xFFF;
        }
        test_all_impls<T>(a, b);
    }
    
    std::cout << "  " << type_name << ": " << tests_passed << " passed, " 
              << tests_failed << " failed\n";
}

int main() {
    std::cout << "=== GCD Baseline Correctness Tests ===\n\n";
    
    int prev_passed, prev_failed;
    
    prev_passed = tests_passed; prev_failed = tests_failed;
    run_test_suite<uint64_t>("uint64_t");
    
    prev_passed = tests_passed; prev_failed = tests_failed;
    run_test_suite<unsigned __int128>("unsigned __int128");
    
    std::cout << "\n=== SUMMARY ===\n";
    std::cout << "Total: " << tests_passed << " passed, " << tests_failed << " failed\n";
    
    if (tests_failed == 0) {
        std::cout << "ALL TESTS PASSED\n";
        return 0;
    } else {
        std::cout << "SOME TESTS FAILED\n";
        return 1;
    }
}
