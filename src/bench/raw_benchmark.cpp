// Raw per-trial benchmark: emits every trial timing for statistical analysis
// Compile: g++ -O3 -march=native -std=c++20 -o raw_benchmark raw_benchmark.cpp
#include "../baselines/gcd_baselines.h"
#include "../novel/branchless_gcd.h"
#include "../novel/lut_gcd.h"
#include "../novel/combined_gcd.h"
#include <iostream>
#include <random>
#include <chrono>
#include <cstdio>
#include <vector>

using Clock = std::chrono::high_resolution_clock;
volatile uint64_t g_sink = 0;
volatile unsigned __int128 g_sink128 = 0;

struct Pair64 { uint64_t a, b; };
struct Pair128 { unsigned __int128 a, b; };

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

int main() {
    const int N = 100000;
    const int TRIALS = 50;  // More trials for bootstrap
    std::mt19937_64 rng(42);

    printf("algorithm,bit_width,distribution,trial,ns_per_op\n");

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

            // Warmup
            uint64_t acc = 0;
            for (int i = 0; i < 1000 && i < (int)data.size(); i++)
                acc ^= algo.fn(data[i].a, data[i].b);
            g_sink = acc;

            for (int trial = 0; trial < TRIALS; trial++) {
                acc = 0;
                auto t0 = Clock::now();
                for (const auto& p : data)
                    acc ^= algo.fn(p.a, p.b);
                auto t1 = Clock::now();
                g_sink = acc;
                double ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
                printf("%s,64,%s,%d,%.4f\n", algo.name, dist, trial, ns / data.size());
            }
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

            unsigned __int128 acc = 0;
            for (int i = 0; i < 1000 && i < (int)data.size(); i++)
                acc ^= algo.fn(data[i].a, data[i].b);
            g_sink128 = acc;

            for (int trial = 0; trial < TRIALS; trial++) {
                acc = 0;
                auto t0 = Clock::now();
                for (const auto& p : data)
                    acc ^= algo.fn(p.a, p.b);
                auto t1 = Clock::now();
                g_sink128 = acc;
                double ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
                printf("%s,128,%s,%d,%.4f\n", algo.name, dist, trial, ns / data.size());
            }
        }
    }

    return 0;
}
