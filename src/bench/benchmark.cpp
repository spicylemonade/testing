// Comprehensive GCD Benchmark Harness
// Compile: g++ -O3 -march=native -std=c++20 -o benchmark benchmark.cpp
// Run: ./benchmark > results.csv
#include "../baselines/gcd_baselines.h"
#include <iostream>
#include <random>
#include <chrono>
#include <vector>
#include <cstring>
#include <cstdio>
#include <functional>
#include <string>

using namespace gcd_baseline;
using Clock = std::chrono::high_resolution_clock;

// Prevent dead-code elimination
volatile uint64_t g_sink = 0;
volatile unsigned __int128 g_sink128 = 0;

template <typename T>
struct Pair { T a, b; };

// ============================================================
// Input generation for different distributions
// ============================================================

template <typename T>
std::vector<Pair<T>> gen_uniform(int n, std::mt19937_64& rng) {
    std::vector<Pair<T>> v(n);
    for (auto& p : v) {
        if constexpr (sizeof(T) <= 8) {
            p.a = rng(); p.b = rng();
        } else {
            p.a = ((unsigned __int128)rng() << 64) | rng();
            p.b = ((unsigned __int128)rng() << 64) | rng();
        }
        // Ensure non-zero for valid GCD
        if (p.a == 0) p.a = 1;
        if (p.b == 0) p.b = 1;
    }
    return v;
}

template <typename T>
std::vector<Pair<T>> gen_skewed(int n, std::mt19937_64& rng) {
    // One operand much larger than the other
    std::vector<Pair<T>> v(n);
    for (auto& p : v) {
        if constexpr (sizeof(T) <= 8) {
            p.a = rng();
            p.b = rng() & 0xFFFF;
        } else {
            p.a = ((unsigned __int128)rng() << 64) | rng();
            p.b = rng() & 0xFFFF;
        }
        if (p.a == 0) p.a = 1;
        if (p.b == 0) p.b = 1;
    }
    return v;
}

template <typename T>
std::vector<Pair<T>> gen_nearly_equal(int n, std::mt19937_64& rng) {
    std::vector<Pair<T>> v(n);
    for (auto& p : v) {
        if constexpr (sizeof(T) <= 8) {
            p.a = rng() | 1;  // ensure odd
            p.b = p.a + 2 * (rng() & 0xFF);  // small even difference
        } else {
            p.a = (((unsigned __int128)rng() << 64) | rng()) | 1;
            p.b = p.a + 2 * (rng() & 0xFF);
        }
        if (p.b == 0) p.b = 1;
    }
    return v;
}

template <typename T>
std::vector<Pair<T>> gen_fibonacci(int n, std::mt19937_64& rng) {
    // Fibonacci-adjacent: worst case for Euclidean algorithm
    std::vector<Pair<T>> v(n);
    for (auto& p : v) {
        T fa = 1, fb = 1;
        // Generate fibonacci numbers up to a random stopping point
        int steps;
        if constexpr (sizeof(T) <= 8)
            steps = 30 + (rng() % 50);
        else
            steps = 60 + (rng() % 100);
        for (int i = 0; i < steps; i++) {
            T t = fa + fb;
            if (t < fb) { break; } // overflow
            fa = fb; fb = t;
        }
        p.a = fb; p.b = fa;
        if (p.a == 0) p.a = 1;
        if (p.b == 0) p.b = 1;
    }
    return v;
}

template <typename T>
std::vector<Pair<T>> gen_coprime(int n, std::mt19937_64& rng) {
    // Generate coprime pairs (both odd, differ by 2)
    std::vector<Pair<T>> v(n);
    for (auto& p : v) {
        if constexpr (sizeof(T) <= 8) {
            p.a = rng() | 1;
            p.b = p.a + 2;
        } else {
            p.a = (((unsigned __int128)rng() << 64) | rng()) | 1;
            p.b = p.a + 2;
        }
    }
    return v;
}

// ============================================================
// Benchmark runner
// ============================================================

template <typename T>
double bench_fn(T (*fn)(T, T), const std::vector<Pair<T>>& data, int warmup_iters, int bench_iters) {
    // Warmup
    T acc = 0;
    for (int i = 0; i < warmup_iters && i < (int)data.size(); i++) {
        acc ^= fn(data[i].a, data[i].b);
    }
    if constexpr (sizeof(T) <= 8) g_sink = acc; else g_sink128 = acc;

    // Benchmark
    auto t0 = Clock::now();
    acc = 0;
    for (int iter = 0; iter < bench_iters; iter++) {
        for (const auto& p : data) {
            acc ^= fn(p.a, p.b);
        }
    }
    auto t1 = Clock::now();
    if constexpr (sizeof(T) <= 8) g_sink = acc; else g_sink128 = acc;

    double total_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
    double ops = (double)data.size() * bench_iters;
    return total_ns / ops;  // ns per operation
}

struct AlgoEntry64 {
    const char* name;
    uint64_t (*fn)(uint64_t, uint64_t);
};

struct AlgoEntry128 {
    const char* name;
    unsigned __int128 (*fn)(unsigned __int128, unsigned __int128);
};

int main() {
    const int N = 100000;  // pairs per distribution
    const int WARMUP = 1000;
    const int ITERS = 10;
    std::mt19937_64 rng(42);

    // CSV header
    printf("algorithm,bit_width,distribution,latency_ns,throughput_ops_sec\n");

    // 64-bit algorithms
    AlgoEntry64 algos64[] = {
        {"euclid",       gcd_euclid<uint64_t>},
        {"stein_classic", gcd_stein_classic<uint64_t>},
        {"binary_ctz",   gcd_binary_ctz<uint64_t>},
        {"binary_opt",   gcd_binary_opt<uint64_t>},
    };

    auto uniform64 = gen_uniform<uint64_t>(N, rng);
    auto skewed64 = gen_skewed<uint64_t>(N, rng);
    auto nearly64 = gen_nearly_equal<uint64_t>(N, rng);
    auto fib64 = gen_fibonacci<uint64_t>(N, rng);
    auto coprime64 = gen_coprime<uint64_t>(N, rng);

    struct { const char* name; std::vector<Pair<uint64_t>>* data; } dists64[] = {
        {"uniform", &uniform64},
        {"skewed", &skewed64},
        {"nearly_equal", &nearly64},
        {"fibonacci", &fib64},
        {"coprime", &coprime64},
    };

    for (auto& algo : algos64) {
        for (auto& dist : dists64) {
            double ns = bench_fn(algo.fn, *dist.data, WARMUP, ITERS);
            double ops_sec = 1e9 / ns;
            printf("%s,64,%s,%.2f,%.0f\n", algo.name, dist.name, ns, ops_sec);
        }
    }

    // 128-bit algorithms
    AlgoEntry128 algos128[] = {
        {"euclid",       gcd_euclid<unsigned __int128>},
        {"stein_classic", gcd_stein_classic<unsigned __int128>},
        {"binary_ctz",   gcd_binary_ctz<unsigned __int128>},
        {"binary_opt",   gcd_binary_opt<unsigned __int128>},
    };

    auto uniform128 = gen_uniform<unsigned __int128>(N, rng);
    auto skewed128 = gen_skewed<unsigned __int128>(N, rng);
    auto nearly128 = gen_nearly_equal<unsigned __int128>(N, rng);
    auto fib128 = gen_fibonacci<unsigned __int128>(N, rng);
    auto coprime128 = gen_coprime<unsigned __int128>(N, rng);

    struct { const char* name; std::vector<Pair<unsigned __int128>>* data; } dists128[] = {
        {"uniform", &uniform128},
        {"skewed", &skewed128},
        {"nearly_equal", &nearly128},
        {"fibonacci", &fib128},
        {"coprime", &coprime128},
    };

    for (auto& algo : algos128) {
        for (auto& dist : dists128) {
            double ns = bench_fn(algo.fn, *dist.data, WARMUP, ITERS);
            double ops_sec = 1e9 / ns;
            printf("%s,128,%s,%.2f,%.0f\n", algo.name, dist.name, ns, ops_sec);
        }
    }

    return 0;
}
