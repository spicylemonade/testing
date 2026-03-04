"""DFA-based lower bound strategy for gamma_2 using optimal automaton search.

The idea (Dancik 1994): Design a DFA that reads symbol pairs (x_i, y_j) from two
input streams and decides when to match characters. The matching rate under the
DFA's strategy gives a lower bound on gamma_2.

State: buffer of h bits from each stream.
At each step:
  - Read the next bit from X and the next bit from Y
  - Based on the current state (buffer contents), decide to either:
    (a) Match: if current heads of both buffers agree, consume both and score 1
    (b) Skip X: advance the X pointer
    (c) Skip Y: advance the Y pointer

The optimal DFA maximizes the expected matching rate, which gives the best
lower bound on gamma_2 for that state space size.

For binary alphabet, with h-symbol lookahead:
  State space: 2^h * 2^h = 4^h states (pairs of h-bit buffers)
  At each state, the DFA must choose one of 3 actions.
  The transition depends on the random next bits from X and Y.

We find the optimal DFA by:
1. Value iteration on the MDP (Markov Decision Process)
2. The average reward (matching rate) is the lower bound

Reference: Dancik (1994), Chapter 3.
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigs
import json
import time
from pathlib import Path
from itertools import product


def optimal_dfa_bound(h, verbose=True):
    """Compute the optimal DFA lower bound for lookahead h.
    
    State: (x_buf, y_buf) where x_buf and y_buf are h-bit buffers.
    x_buf and y_buf represent the next h characters available from each string.
    
    At each step, the DFA can:
    - MATCH: if x_buf[0] == y_buf[0], consume both first bits, score +1
    - SKIP_X: consume x_buf[0], no score
    - SKIP_Y: consume y_buf[0], no score
    
    After consuming, a new random bit is appended at the end.
    
    We use value iteration to find the optimal policy.
    The average reward = the DFA lower bound on gamma_2.
    """
    num_states = (1 << h) * (1 << h)
    
    if verbose:
        print(f"  h={h}: {num_states} states, building MDP...", flush=True)
    
    # For each state and action, compute transition probabilities and rewards
    # Actions: 0=SKIP_X, 1=SKIP_Y, 2=MATCH (only if heads agree)
    
    # Pre-compute transitions
    # State encoding: s = x_buf * 2^h + y_buf
    mask = (1 << h) - 1
    
    # Value iteration
    V = np.zeros(num_states, dtype=np.float64)
    policy = np.zeros(num_states, dtype=np.int8)
    
    # Relative value iteration (RVI):
    # V(s) = max_a [r(s,a) + sum_s' P(s'|s,a) V(s') ] - V(ref)
    # where ref is a fixed reference state
    # The average reward rho = V(ref_old) - V(ref_new) converges to the true gain
    
    ref_state = 0  # Reference state for RVI
    
    for iteration in range(10000):
        V_new = np.full(num_states, -np.inf, dtype=np.float64)
        policy_new = np.zeros(num_states, dtype=np.int8)
        
        for s in range(num_states):
            x_buf = s >> h
            y_buf = s & mask
            x_head = x_buf & 1
            y_head = y_buf & 1
            
            best_val = -np.inf
            best_act = 0
            
            # Action 0: SKIP_X (advance X pointer by 1)
            val = 0.0
            for new_bit in range(2):
                new_x = ((x_buf >> 1) | (new_bit << (h-1))) & mask
                new_s = (new_x << h) | y_buf
                val += 0.5 * V[new_s]
            if val > best_val:
                best_val = val
                best_act = 0
            
            # Action 1: SKIP_Y (advance Y pointer by 1)
            val = 0.0
            for new_bit in range(2):
                new_y = ((y_buf >> 1) | (new_bit << (h-1))) & mask
                new_s = (x_buf << h) | new_y
                val += 0.5 * V[new_s]
            if val > best_val:
                best_val = val
                best_act = 1
            
            # Action 2: MATCH (only if heads agree)
            if x_head == y_head:
                val = 1.0  # Reward for matching
                for new_bit_x in range(2):
                    for new_bit_y in range(2):
                        new_x = ((x_buf >> 1) | (new_bit_x << (h-1))) & mask
                        new_y = ((y_buf >> 1) | (new_bit_y << (h-1))) & mask
                        new_s = (new_x << h) | new_y
                        val += 0.25 * V[new_s]
                if val > best_val:
                    best_val = val
                    best_act = 2
            
            V_new[s] = best_val
            policy_new[s] = best_act
        
        # RVI: subtract V of reference state to keep values bounded
        V_new -= V_new[ref_state]
        
        # Check convergence via span seminorm
        diff_vec = V_new - V
        span = diff_vec.max() - diff_vec.min()
        
        V = V_new
        policy = policy_new
        
        if span < 1e-12 and iteration > 50:
            break
    
    # Compute the actual matching rate under the converged policy
    # Build the transition matrix under the policy and find stationary distribution
    # Then compute expected reward
    
    # Build transition matrix
    rows, cols, vals = [], [], []
    rewards = np.zeros(num_states, dtype=np.float64)
    
    for s in range(num_states):
        x_buf = s >> h
        y_buf = s & mask
        x_head = x_buf & 1
        y_head = y_buf & 1
        act = policy[s]
        
        if act == 0:  # SKIP_X
            rewards[s] = 0.0
            for new_bit in range(2):
                new_x = ((x_buf >> 1) | (new_bit << (h-1))) & mask
                new_s = (new_x << h) | y_buf
                rows.append(s)
                cols.append(new_s)
                vals.append(0.5)
        elif act == 1:  # SKIP_Y
            rewards[s] = 0.0
            for new_bit in range(2):
                new_y = ((y_buf >> 1) | (new_bit << (h-1))) & mask
                new_s = (x_buf << h) | new_y
                rows.append(s)
                cols.append(new_s)
                vals.append(0.5)
        elif act == 2:  # MATCH
            rewards[s] = 1.0
            for new_bit_x in range(2):
                for new_bit_y in range(2):
                    new_x = ((x_buf >> 1) | (new_bit_x << (h-1))) & mask
                    new_y = ((y_buf >> 1) | (new_bit_y << (h-1))) & mask
                    new_s = (new_x << h) | new_y
                    rows.append(s)
                    cols.append(new_s)
                    vals.append(0.25)
    
    T = sparse.csr_matrix((vals, (rows, cols)), shape=(num_states, num_states))
    
    # Find stationary distribution via power iteration
    pi = np.ones(num_states) / num_states
    for _ in range(5000):
        pi_new = pi @ T
        pi_new /= pi_new.sum()
        if np.max(np.abs(pi_new - pi)) < 1e-15:
            break
        pi = pi_new
    
    # Matching rate = expected reward under stationary distribution
    matching_rate = float(pi @ rewards)
    
    # But this is the rate per "step", and each step advances one or both pointers.
    # We need to convert to rate per character.
    # In each step, we consume 1 character from X (SKIP_X or MATCH) or 1 from Y (SKIP_Y).
    # For MATCH, we consume 1 from each.
    
    # Expected characters consumed from X per step:
    x_consumed = np.zeros(num_states)
    y_consumed = np.zeros(num_states)
    for s in range(num_states):
        act = policy[s]
        if act == 0:  # SKIP_X
            x_consumed[s] = 1.0
            y_consumed[s] = 0.0
        elif act == 1:  # SKIP_Y
            x_consumed[s] = 0.0
            y_consumed[s] = 1.0
        elif act == 2:  # MATCH
            x_consumed[s] = 1.0
            y_consumed[s] = 1.0
    
    avg_x_consumed = float(pi @ x_consumed)
    avg_y_consumed = float(pi @ y_consumed)
    avg_matched = matching_rate
    
    # The DFA processes both strings. After n steps, it has consumed
    # ~n * avg_x_consumed chars from X and ~n * avg_y_consumed from Y.
    # It has matched ~n * avg_matched characters.
    # The effective LCS rate relative to string length is:
    # gamma_lower = avg_matched / max(avg_x_consumed, avg_y_consumed)
    # Actually, both strings have the same length n, so we need the rate
    # at which both strings are fully consumed. This is:
    # gamma_lower = avg_matched / max(avg_x_consumed, avg_y_consumed) * min(avg_x_consumed, avg_y_consumed) / max(avg_x_consumed, avg_y_consumed)
    # 
    # More precisely: if the DFA consumes X at rate r_x and Y at rate r_y per step,
    # and matches at rate m per step, then to process strings of length n:
    # - Number of steps ≈ n / r_x (X is fully consumed)
    # - Y consumed ≈ n * r_y / r_x (might be less or more than n)
    # 
    # For a valid LCS strategy, we need both strings fully processed.
    # The binding constraint is: steps = n / min(r_x, r_y) ... no, that's wrong.
    # 
    # Actually, the DFA must process both strings completely. At each step it
    # advances at least one stream. The rate per character of the longer string
    # (which determines the normalization) gives the bound.
    #
    # Since both strings are length n, the bound is:
    # gamma_lower >= m / (r_x + r_y - m) ... no.
    #
    # Let me think again. After N steps:
    # - Characters consumed from X: N * r_x
    # - Characters consumed from Y: N * r_y
    # - Characters matched: N * m
    # 
    # We need N * r_x = n and N * r_y = n (process both strings fully).
    # This is only possible if r_x = r_y. By symmetry of the problem, the 
    # optimal policy should have r_x = r_y. Let's check.
    #
    # If r_x != r_y, the faster stream finishes first, and we'd need to 
    # only use SKIP on the slower stream to catch up. The effective rate is:
    # LCS length / n = m / max(r_x, r_y)
    
    gamma_lower = avg_matched / max(avg_x_consumed, avg_y_consumed)
    
    if verbose:
        print(f"    Matching rate per step: {avg_matched:.8f}")
        print(f"    X consumed per step: {avg_x_consumed:.8f}")
        print(f"    Y consumed per step: {avg_y_consumed:.8f}")
        print(f"    Lower bound: {gamma_lower:.8f}")
        
        # Describe policy
        match_states = sum(1 for s in range(num_states) if policy[s] == 2)
        skip_x_states = sum(1 for s in range(num_states) if policy[s] == 0)
        skip_y_states = sum(1 for s in range(num_states) if policy[s] == 1)
        print(f"    Policy: {match_states} MATCH, {skip_x_states} SKIP_X, {skip_y_states} SKIP_Y states")
    
    return gamma_lower, matching_rate, policy, iteration


def main():
    print("DFA Lower Bound via Optimal Automaton Search")
    print("=" * 60)
    
    results = {}
    
    for h in range(2, 7):
        t0 = time.time()
        print(f"\nh={h} (state space: {4**h})")
        
        gamma_lower, match_rate, policy, iters = optimal_dfa_bound(h)
        elapsed = time.time() - t0
        
        results[str(h)] = {
            "h": h,
            "state_space_size": 4**h,
            "lower_bound": round(gamma_lower, 10),
            "match_rate_per_step": round(match_rate, 10),
            "num_iterations": iters,
            "elapsed_seconds": round(elapsed, 2)
        }
        
        print(f"  Result: gamma_2 >= {gamma_lower:.10f} ({elapsed:.1f}s, {iters} iterations)")
    
    # Summary
    best_h = max(results.keys(), key=lambda k: results[k]["lower_bound"])
    best_bound = results[best_h]["lower_bound"]
    
    print(f"\n{'='*60}")
    print(f"Best lower bound: gamma_2 >= {best_bound:.10f} (at h={best_h})")
    print(f"Dancik (1994) achieved: 0.773911")
    print(f"Heineman et al. (2024): 0.792665992")
    
    output = {
        "description": "DFA-based lower bounds on gamma_2 via optimal automaton search",
        "method": "MDP value iteration to find optimal DFA policy",
        "results": results,
        "best_bound": best_bound,
        "best_h": int(best_h),
        "comparison": {
            "dancik_1994": 0.773911,
            "lueker_2009_lower": 0.788071,
            "heineman_2024": 0.792665992
        }
    }
    
    outpath = Path(__file__).parent / "dfa_lower_bounds.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {outpath}")


if __name__ == "__main__":
    main()
