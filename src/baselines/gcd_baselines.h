#pragma once
// Baseline GCD implementations for benchmarking
// Compile: g++ -O3 -march=native -std=c++20

#include <cstdint>
#include <cstdlib>
#include <algorithm>
#include <type_traits>
#include <bit>

namespace gcd_baseline {

// ============================================================
// Helpers for 128-bit support
// ============================================================

inline int ctz_u128(unsigned __int128 x) {
    uint64_t lo = static_cast<uint64_t>(x);
    if (lo) return __builtin_ctzll(lo);
    uint64_t hi = static_cast<uint64_t>(x >> 64);
    return 64 + __builtin_ctzll(hi);
}

// std::make_signed doesn't support __int128 in all compilers
template <typename T> struct make_signed_helper { using type = std::make_signed_t<T>; };
template <> struct make_signed_helper<unsigned __int128> { using type = __int128; };
template <typename T> using signed_t = typename make_signed_helper<T>::type;

// ============================================================
// 1. Euclidean GCD (std::gcd equivalent)
// ============================================================

template <typename T>
__attribute__((noinline))
T gcd_euclid(T a, T b) {
    while (b) {
        T t = b;
        b = a % b;
        a = t;
    }
    return a;
}

// ============================================================
// 2. Stein's Classic Binary GCD (branchy)
// ============================================================

template <typename T>
__attribute__((noinline))
T gcd_stein_classic(T a, T b) {
    if (a == 0) return b;
    if (b == 0) return a;

    // Factor out common powers of 2
    int shift;
    if constexpr (sizeof(T) <= 8) {
        shift = __builtin_ctzll(static_cast<uint64_t>(a | b));
    } else {
        shift = ctz_u128(a | b);
    }
    a >>= shift;
    b >>= shift;

    // Remove remaining factors of 2 from a
    if constexpr (sizeof(T) <= 8) {
        a >>= __builtin_ctzll(static_cast<uint64_t>(a));
    } else {
        a >>= ctz_u128(a);
    }

    while (b != 0) {
        // Remove factors of 2 from b
        if constexpr (sizeof(T) <= 8) {
            b >>= __builtin_ctzll(static_cast<uint64_t>(b));
        } else {
            b >>= ctz_u128(b);
        }
        // Ensure a <= b, then subtract
        if (a > b) {
            T t = a; a = b; b = t;
        }
        b -= a;
    }
    return a << shift;
}

// ============================================================
// 3. CTZ-Optimized Binary GCD (Lemire/Corderoy variant)
//    Uses __builtin_ctzll but with TZCNT after ABS
// ============================================================

template <typename T>
__attribute__((noinline))
T gcd_binary_ctz(T a, T b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az, bz, shift;
    if constexpr (sizeof(T) <= 8) {
        az = __builtin_ctzll(static_cast<uint64_t>(a));
        bz = __builtin_ctzll(static_cast<uint64_t>(b));
    } else {
        az = ctz_u128(a);
        bz = ctz_u128(b);
    }
    shift = std::min(az, bz);
    a >>= az;
    b >>= bz;

    while (a != 0) {
        // Compute diff, min, abs — unsigned safe version
        T d;
        if (a > b) {
            d = a - b;
            a = b;
        } else {
            d = b - a;
        }
        b = a;
        a = d;
        if constexpr (sizeof(T) <= 8) {
            a >>= __builtin_ctzll(static_cast<uint64_t>(a));
        } else {
            if (a != 0) a >>= ctz_u128(a);
        }
    }
    return b << shift;
}

// ============================================================
// 4. Algorithmica Dependency-Optimized Binary GCD
//    Key optimization: TZCNT before ABS (on raw difference)
//    ctz(x) == ctz(-x) for all x != 0, so we can compute
//    TZCNT on the raw (unsigned wrapping) difference.
// ============================================================

template <typename T>
__attribute__((noinline))
T gcd_binary_opt(T a, T b) {
    if (a == 0) return b;
    if (b == 0) return a;

    int az, bz, shift;
    if constexpr (sizeof(T) <= 8) {
        az = __builtin_ctzll(static_cast<uint64_t>(a));
        bz = __builtin_ctzll(static_cast<uint64_t>(b));
    } else {
        az = ctz_u128(a);
        bz = ctz_u128(b);
    }
    shift = std::min(az, bz);
    b >>= bz;  // Note: only shift b initially

    while (a != 0) {
        a >>= az;  // Apply previous iteration's shift
        // Compute difference (unsigned wrap-around is fine for ctz)
        T diff = b - a;  // unsigned subtraction
        // TZCNT on raw difference (before abs) — KEY OPTIMIZATION
        // ctz(b-a) == ctz(a-b) because trailing zeros are preserved by negation
        if constexpr (sizeof(T) <= 8) {
            az = __builtin_ctzll(static_cast<uint64_t>(diff));
        } else {
            az = (diff != 0) ? ctz_u128(diff) : 1;
        }
        // min and abs-diff without signed overflow
        if (a < b) {
            b = a;
            a = diff;   // b - a, which is positive
        } else {
            a = a - b;  // a - b, which is positive (diff = b-a was negative/wrapped)
        }
    }
    return b << shift;
}

} // namespace gcd_baseline
