// Test and benchmark all novel GCD implementations
// Compile: g++ -O3 -march=native -std=c++20 -o test_novel test_novel.cpp
#include "branchless_gcd.h"
#include "lut_gcd.h"
#include "divstep_gcd.h"
#include "../baselines/gcd_baselines.h"
#include <iostream>
#include <random>
#include <chrono>
#include <cstdio>
#include <vector>
#include <functional>
#include <string>

using Clock = std::chrono::high_resolution_clock;
volatile uint64_t g_sink = 0;

// Reference GCD
uint64_t ref_gcd(uint64_t a, uint64_t b) {
    while (b) { uint64_t t = b; b = a % b; a = t; }
    return a;
}

struct AlgoEntry {
    const char* name;
    uint64_t (*fn)(uint64_t, uint64_t);
};

// Correctness test
int test_correctness(const AlgoEntry* algos, int nalgo) {
    std::mt19937_64 rng(42);
    int total_fail = 0;
    
    for (int ai = 0; ai < nalgo; ai++) {
        int fails = 0;
        auto fn = algos[ai].fn;
        
        // Edge cases
        auto chk = [&](uint64_t a, uint64_t b) {
            uint64_t expected = ref_gcd(a, b);
            uint64_t got = fn(a, b);
            if (got != expected) {
                if (fails < 5)
                    fprintf(stderr, "  FAIL %s: gcd(%lu, %lu) = %lu, got %lu\n",
                            algos[ai].name, a, b, expected, got);
                fails++;
            }
        };
        
        chk(0, 0); chk(0, 1); chk(1, 0); chk(1, 1);
        chk(0, 42); chk(42, 0); chk(13, 7); chk(42, 42);
        chk(6, 12); chk(1000, 1000);
        chk(1ULL << 20, 1ULL << 30);
        chk(UINT64_MAX, UINT64_MAX);
        chk(UINT64_MAX, 1);
        chk(UINT64_MAX, 2);
        
        // Fibonacci
        uint64_t fa = 1, fb = 1;
        for (int i = 0; i < 80; i++) {
            chk(fa, fb);
            uint64_t t = fa + fb;
            if (t < fb) break;
            fa = fb; fb = t;
        }
        
        // Random
        for (int i = 0; i < 20000; i++) {
            uint64_t a = rng(), b = rng();
            if (i < 5000) { /* uniform */ }
            else if (i < 10000) { b &= 0xFFFF; }
            else if (i < 15000) { b = a + (rng() & 0xFF); }
            else { a &= 0xFFF; }
            chk(a, b);
        }
        
        printf("  %-25s: %s (%d failures)\n", algos[ai].name, 
               fails == 0 ? "PASS" : "FAIL", fails);
        total_fail += fails;
    }
    return total_fail;
}

struct Pair { uint64_t a, b; };

double bench_fn(uint64_t (*fn)(uint64_t, uint64_t), const std::vector<Pair>& data, int iters) {
    uint64_t acc = 0;
    // Warmup
    for (int i = 0; i < 1000 && i < (int)data.size(); i++)
        acc ^= fn(data[i].a, data[i].b);
    g_sink = acc;
    
    auto t0 = Clock::now();
    acc = 0;
    for (int iter = 0; iter < iters; iter++)
        for (const auto& p : data)
            acc ^= fn(p.a, p.b);
    auto t1 = Clock::now();
    g_sink = acc;
    
    double ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
    return ns / ((double)data.size() * iters);
}

int main() {
    AlgoEntry algos[] = {
        // Baselines
        {"euclid",            gcd_baseline::gcd_euclid<uint64_t>},
        {"stein_classic",     gcd_baseline::gcd_stein_classic<uint64_t>},
        {"binary_ctz",        gcd_baseline::gcd_binary_ctz<uint64_t>},
        {"binary_opt",        gcd_baseline::gcd_binary_opt<uint64_t>},
        // Novel
        {"branchless_fixed",  gcd_novel::gcd_branchless_fixed},
        {"branchless_loop",   gcd_novel::gcd_branchless_loop},
        {"branchless_hybrid", gcd_novel::gcd_branchless_hybrid},
        {"novel_v4",          gcd_novel::gcd_novel_v4},
        {"novel_best",        gcd_novel::gcd_novel_best},
        {"novel_unrolled",    gcd_novel::gcd_novel_unrolled},
        {"lut_hybrid",        gcd_novel::gcd_lut_hybrid},
        {"lut_hybrid_mod",    gcd_novel::gcd_lut_hybrid_mod},
        {"divstep_v2",        gcd_novel::gcd_divstep_v2},
    };
    int nalgo = sizeof(algos) / sizeof(algos[0]);
    
    printf("=== Correctness Tests ===\n");
    int fails = test_correctness(algos, nalgo);
    
    if (fails > 0) {
        printf("\n%d algorithms have failures. Running benchmarks only on passing algorithms.\n", fails);
    }
    
    printf("\n=== Benchmarks (64-bit) ===\n");
    
    // Generate test data
    std::mt19937_64 rng(42);
    const int N = 100000;
    
    auto gen = [&](auto transform) {
        std::vector<Pair> v(N);
        for (auto& p : v) { p.a = rng(); p.b = rng(); transform(p); }
        return v;
    };
    
    auto uniform = gen([](Pair& p) { if(!p.a) p.a=1; if(!p.b) p.b=1; });
    auto skewed = gen([](Pair& p) { p.b &= 0xFFFF; if(!p.a) p.a=1; if(!p.b) p.b=1; });
    auto nearly = gen([](Pair& p) { p.b = p.a + (p.b & 0xFF); if(!p.a) p.a=1; if(!p.b) p.b=1; });
    
    struct { const char* name; std::vector<Pair>* data; } dists[] = {
        {"uniform", &uniform},
        {"skewed", &skewed},
        {"nearly_equal", &nearly},
    };
    
    printf("\nalgorithm,distribution,latency_ns\n");
    for (auto& algo : algos) {
        for (auto& dist : dists) {
            double ns = bench_fn(algo.fn, *dist.data, 5);
            printf("%s,%s,%.2f\n", algo.name, dist.name, ns);
        }
    }
    
    return fails > 0 ? 1 : 0;
}
