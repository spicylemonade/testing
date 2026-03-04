# 006: Binary Representation Sieve

## Overview

The binary representation of a number completely determines the first k steps of its Collatz trajectory (where k is the number of bits examined). This creates a natural "binary template" sieve: precompute optimal low-order bit patterns and search only numbers matching those patterns.

## Key Insight

Numbers of the form n = ...1111 (ending in k ones in binary) undergo k consecutive odd steps, causing the trajectory to ascend by a factor of approximately (3/2)^k. This is because:
- T(n) = (3n+1)/2 when n is odd
- If n ends in 1, so does (3n+1)/2 (with probability ~1/2)
- Consecutive odd steps compound the 3/2 multiplier

## Binary Template Hierarchy

1. **Level 0**: All odd numbers (1 bit: ends in 1) - 50% of integers
2. **Level 1**: Numbers ending ...11 - 25% of integers  
3. **Level k**: Numbers ending in k ones - 2^{-k} of integers
4. **Optimal templates**: Specific k-bit patterns that maximize completeness

## Implementation Backlog

1. [ ] Enumerate all 2^16 suffixes and compute Collatz statistics
2. [ ] Rank by completeness C = odd_steps/even_steps
3. [ ] Build trie data structure for efficient pattern matching
4. [ ] Validate against known delay records
5. [ ] Extend to 2^20 and 2^24 with entropy filtering
6. [ ] Combine with the modular sieve for hybrid acceleration
