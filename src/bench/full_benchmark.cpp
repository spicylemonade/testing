// Full comparative benchmark: all baselines + novel algorithms
// Compile: g++ -O3 -march=native -std=c++20 -o full_benchmark full_benchmark.cpp
#include "../baselines/gcd_baselines.h"
#include "../novel/branchless_gcd.h"
#include "../novel/lut_gcd.h"
#include "../novel/combined_gcd.h"
#include <iostream>
#include <random>
#include <chrono>
#include <cstdio>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>

using Clock = std::chrono::high_resolution_clock;
volatile uint64_t g_sink = 0;
volatile unsigned __int128 g_sink128 = 0;

struct Pair64 { uint64_t a, b; };
struct Pair128 { unsigned __int128 a, b; };

// ============================================================
// Input generators
// ============================================================

std::vector<Pair64> gen64(int n, std::mt19937_64& rng, const char* dist) {
    std::vector<Pair64> v(n);
    for (auto& p : v) {
        p.a = rng(); p.b = rng();
        if (std::string(dist) == "skewed") p.b &= 0xFFFF;
        else if (std::string(dist) == "nearly_equal") p.b = p.a + (p.b & 0xFF);
        else if (std::string(dist) == "coprime") { p.a |= 1; p.b = p.a + 2; }
        if (!p.a) p.a = 1; if (!p.b) p.b = 1;
    }
    if (std::string(dist) == "fibonacci") {
        for (int i = 0; i < n; i++) {
            uint64_t fa = 1, fb = 1;
            int steps = 30 + (rng() % 50);
            for (int j = 0; j < steps; j++) {
                uint64_t t = fa + fb;
                if (t < fb) break;
                fa = fb; fb = t;
            }
            v[i] = {fb, fa};
        }
    }
    return v;
}

std::vector<Pair128> gen128(int n, std::mt19937_64& rng, const char* dist) {
    std::vector<Pair128> v(n);
    for (auto& p : v) {
        p.a = ((unsigned __int128)rng() << 64) | rng();
        p.b = ((unsigned __int128)rng() << 64) | rng();
        if (std::string(dist) == "skewed") p.b &= 0xFFFF;
        else if (std::string(dist) == "nearly_equal") p.b = p.a + (p.b & 0xFF);
        else if (std::string(dist) == "coprime") { p.a |= 1; p.b = p.a + 2; }
        if (!p.a) p.a = 1; if (!p.b) p.b = 1;
    }
    if (std::string(dist) == "fibonacci") {
        for (int i = 0; i < n; i++) {
            unsigned __int128 fa = 1, fb = 1;
            int steps = 60 + (rng() % 100);
            for (int j = 0; j < steps; j++) {
                unsigned __int128 t = fa + fb;
                if (t < fb) break;
                fa = fb; fb = t;
            }
            v[i] = {fb, fa};
        }
    }
    return v;
}

// ============================================================
// Benchmark with statistical summary
// ============================================================

template <typename T, typename Pair>
struct BenchResult {
    double mean_ns, median_ns, p5_ns, p95_ns, stddev_ns;
};

template <typename T, typename Pair>
BenchResult<T, Pair> bench_stat(T (*fn)(T, T), const std::vector<Pair>& data, int trials) {
    std::vector<double> samples;
    
    // Warmup
    T acc = 0;
    for (int i = 0; i < 1000 && i < (int)data.size(); i++)
        acc ^= fn(data[i].a, data[i].b);
    if constexpr (sizeof(T) <= 8) g_sink = acc; else g_sink128 = acc;
    
    for (int trial = 0; trial < trials; trial++) {
        auto t0 = Clock::now();
        acc = 0;
        for (const auto& p : data)
            acc ^= fn(p.a, p.b);
        auto t1 = Clock::now();
        if constexpr (sizeof(T) <= 8) g_sink = acc; else g_sink128 = acc;
        
        double ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
        samples.push_back(ns / data.size());
    }
    
    std::sort(samples.begin(), samples.end());
    
    double sum = 0; for (auto s : samples) sum += s;
    double mean = sum / samples.size();
    double var = 0; for (auto s : samples) var += (s - mean) * (s - mean);
    
    BenchResult<T, Pair> r;
    r.mean_ns = mean;
    r.median_ns = samples[samples.size() / 2];
    r.p5_ns = samples[(int)(samples.size() * 0.05)];
    r.p95_ns = samples[(int)(samples.size() * 0.95)];
    r.stddev_ns = std::sqrt(var / samples.size());
    return r;
}

int main() {
    const int N = 100000;
    const int TRIALS = 20;
    std::mt19937_64 rng(42);
    
    // CSV header
    printf("algorithm,bit_width,distribution,mean_ns,median_ns,p5_ns,p95_ns,stddev_ns,throughput_ops_sec\n");
    
    // 64-bit algorithms
    struct { const char* name; uint64_t (*fn)(uint64_t, uint64_t); } algos64[] = {
        {"euclid",            gcd_baseline::gcd_euclid<uint64_t>},
        {"stein_classic",     gcd_baseline::gcd_stein_classic<uint64_t>},
        {"binary_ctz",        gcd_baseline::gcd_binary_ctz<uint64_t>},
        {"binary_opt",        gcd_baseline::gcd_binary_opt<uint64_t>},
        {"branchless_hybrid", gcd_novel::gcd_branchless_hybrid},
        {"novel_best",        gcd_novel::gcd_novel_best},
        {"lut_hybrid",        gcd_novel::gcd_lut_hybrid},
        {"lut_hybrid_mod",    gcd_novel::gcd_lut_hybrid_mod},
        {"combined",          gcd_novel::gcd_combined},
        {"combined_nolut",    gcd_novel::gcd_combined_nolut},
    };
    
    const char* dists[] = {"uniform", "skewed", "nearly_equal", "fibonacci", "coprime"};
    
    for (auto& algo : algos64) {
        for (auto& dist : dists) {
            rng.seed(42);
            auto data = gen64(N, rng, dist);
            auto r = bench_stat<uint64_t, Pair64>(algo.fn, data, TRIALS);
            printf("%s,64,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.0f\n",
                   algo.name, dist, r.mean_ns, r.median_ns, r.p5_ns, r.p95_ns, r.stddev_ns,
                   1e9 / r.median_ns);
        }
    }
    
    // 128-bit algorithms
    struct { const char* name; unsigned __int128 (*fn)(unsigned __int128, unsigned __int128); } algos128[] = {
        {"euclid",            gcd_baseline::gcd_euclid<unsigned __int128>},
        {"stein_classic",     gcd_baseline::gcd_stein_classic<unsigned __int128>},
        {"binary_ctz",        gcd_baseline::gcd_binary_ctz<unsigned __int128>},
        {"binary_opt",        gcd_baseline::gcd_binary_opt<unsigned __int128>},
        {"combined_128",      gcd_novel::gcd_combined_128},
    };
    
    for (auto& algo : algos128) {
        for (auto& dist : dists) {
            rng.seed(42);
            auto data = gen128(N, rng, dist);
            auto r = bench_stat<unsigned __int128, Pair128>(algo.fn, data, TRIALS);
            printf("%s,128,%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.0f\n",
                   algo.name, dist, r.mean_ns, r.median_ns, r.p5_ns, r.p95_ns, r.stddev_ns,
                   1e9 / r.median_ns);
        }
    }
    
    return 0;
}
