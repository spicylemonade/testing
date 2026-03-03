// Assembly analysis: compile with g++ -O3 -march=native -S -o asm_analysis.s asm_analysis.cpp
#include <cstdint>
#include <cstdlib>
#include <algorithm>
#include <numeric>

// Version 1: Euclidean (std::gcd equivalent)
__attribute__((noinline))
uint64_t gcd_euclid(uint64_t a, uint64_t b) {
    while (b) {
        uint64_t t = b;
        b = a % b;
        a = t;
    }
    return a;
}

// Version 2: Naive binary GCD (branchy)
__attribute__((noinline))
uint64_t gcd_binary_branchy(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int shift = __builtin_ctzll(a | b);
    a >>= __builtin_ctzll(a);

    while (b != 0) {
        b >>= __builtin_ctzll(b);
        if (a > b) { uint64_t t = a; a = b; b = t; }
        b -= a;
    }
    return a << shift;
}

// Version 3: Algorithmica-style (TZCNT after ABS, non-optimal)
__attribute__((noinline))
uint64_t gcd_binary_cmov_v1(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = std::min(az, bz);
    a >>= az;
    b >>= bz;

    while (a != 0) {
        int64_t diff = (int64_t)a - (int64_t)b;
        b = std::min(a, b);
        a = (uint64_t)std::abs(diff);
        a >>= __builtin_ctzll(a);
    }
    return b << shift;
}

// Version 4: Algorithmica-style optimized (TZCNT before ABS)
__attribute__((noinline))
uint64_t gcd_binary_cmov_v2(uint64_t a, uint64_t b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az = __builtin_ctzll(a);
    int bz = __builtin_ctzll(b);
    int shift = std::min(az, bz);
    b >>= bz;

    while (a != 0) {
        a >>= az;
        int64_t diff = (int64_t)b - (int64_t)a;
        az = __builtin_ctzll(diff);
        b = std::min(a, b);
        a = (uint64_t)std::abs(diff);
    }
    return b << shift;
}

// Prevent optimization away
volatile uint64_t sink;

int main() {
    sink = gcd_euclid(1071, 462);
    sink = gcd_binary_branchy(1071, 462);
    sink = gcd_binary_cmov_v1(1071, 462);
    sink = gcd_binary_cmov_v2(1071, 462);
    return 0;
}
