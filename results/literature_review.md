# BB(6) State-of-the-Art: Comprehensive Literature Review

## 1. The Busy Beaver Function

The Busy Beaver function BB(n), introduced by Tibor Rado in 1962, asks: what is the maximum number of 1s that a halting n-state, 2-symbol Turing machine can write on an initially blank tape? The related function S(n) asks for the maximum number of steps such a machine can take before halting. Both are famously uncomputable — they grow faster than any computable function — making them central objects of study in computability theory.

The known exact values are:
- BB(1) = 1, S(1) = 1
- BB(2) = 4, S(2) = 6
- BB(3) = 6, S(3) = 21
- BB(4) = 13, S(4) = 107
- BB(5) = 47,176,870, S(5) = 47,176,870 (proven July 2, 2024)
- BB(6) = unknown; current lower bound: > 2↑↑↑5 (pentation level)

## 2. Current Best Known BB(6) Lower Bound

### The Record: BB(6) > 2↑↑↑5

The current BB(6) champion was discovered by **mxdys** (pseudonymous researcher, GitHub: ccz181078) in **June 2025**. The machine is:

```
1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE
```

In standard notation, this encodes a 6-state, 2-symbol Turing machine whose behavior produces a number of 1s on the tape exceeding 2↑↑↑5 — that is, 2 pentated to 5, or equivalently 2 tetrated to (2 tetrated to (2 tetrated to (2 tetrated to 2))). This is a number so vast it cannot be meaningfully compared to any quantity in physics — it dwarfs the number of particles in the observable universe by an unfathomable margin.

Partial Coq/Rocq proofs for this machine are available at https://github.com/ccz181078/busycoq/tree/BB6.

### Timeline of BB(6) Lower Bounds

| Date | Discoverer | Lower Bound | Notes |
|------|-----------|-------------|-------|
| 1990 | Marxen & Buntrock | > 8,690,333,381,690,951 | |
| 2010 | Pavel Kropitz | > 3.1 × 10^10,566 | |
| May 13, 2022 | Shawn Ligocki | > 10^78,913 | |
| May 15, 2022 | Pavel Kropitz | > 10^197,282 | |
| May 22, 2022 | Pavel Kropitz | > 10^1,292,913,985 | |
| May 27, 2022 | Shawn Ligocki | > 10↑↑5 | First tetrational-level bound |
| May 30, 2022 | Pavel Kropitz | > 10↑↑15 | "Kropitz champion" |
| June 2025 | mxdys | > 10↑↑10,000,000 | Intermediate discovery |
| June 2025 | mxdys | > 2↑↑↑5 | Current record (pentation level) |

### How the Champion Works

The mxdys champion uses **Shift Overflow Counters** — a technique where the machine repeatedly increments a binary counter on the tape until it "overflows" (requires an extra digit). At overflow points, new behavior triggers. This mechanism computes exponential functions (binary counters take exponentially many steps to overflow). With one extra loop on top, you get tetration-level helper functions. The machine applies a Collatz-like test at each iteration, halting on certain remainders and repeating otherwise.

## 3. The BB(5) Proof: A Landmark Achievement

### Result: BB(5) = S(5) = 47,176,870

The 5-state champion Turing machine was discovered by Heiner Marxen and Jürgen Buntrock in September 1989. It runs for exactly 47,176,870 steps and writes 4,098 ones on the tape. The conjecture that this was the true BB(5) value stood for 35 years.

### The bbchallenge.org Proof (July 2, 2024)

The proof was announced on July 2, 2024, by the **bbchallenge.org collaboration** — a distributed, open-source project founded by **Tristan Sterin** (Maynooth University / prgm.dev, Paris). The proof is entirely machine-checked in the **Coq (now Rocq)** proof assistant.

### Method

The proof required deciding, for every one of **181,385,789** 5-state Turing machines (after TNF reduction from the theoretical space of trillions), whether it halts or loops forever. This was accomplished using:

1. **Tree Normal Form (TNF) enumeration**: Reduced the search space by canonicalizing equivalent machines using Brady's algorithm.
2. **Automated deciders**: Programs that classify TMs as HALT, NONHALT, or UNKNOWN. Categories include:
   - Cyclers / Translated Cyclers (detect periodic behavior)
   - Backward Reasoning (prove unreachability of halt state)
   - CTL (Closed Tape Language analysis)
   - Finite Automata Reduction (FAR)
   - Inductive Rules / Bouncers
3. **Formal Coq proofs**: Every classification was formalized and machine-checked.
4. **Community collaboration**: ~18+ named contributors plus the broader community.

The hardest single case was **Skelet #17** (`1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA`), resolved by Maja Kądziołka in a dedicated paper (arXiv:2407.02426, July 2024).

### Publication

The full paper was published September 15, 2025 as arXiv:2509.12337: "Determination of the fifth Busy Beaver value" by the bbchallenge Collaboration (19 authors: Justin Blanchard, Daniel Briggs, Konrad Deka, Nathan Fenner, Yannick Forster, Georgi Georgiev, Matthew L. House, Rachel Hunter, Iijil, Maja Kądziołka, Pavel Kropitz, Shawn Ligocki, mxdys, Mateusz Naściszewski, savask, Tristan Sterin, Chris Xu, Jason Yuen, Theo Zimmermann).

## 4. Active Researchers and Groups

### Individual Researchers

1. **Tristan Sterin** — Founder and organizer of bbchallenge.org. Former PhD student under Damien Woods at Maynooth University, Ireland. Now at prgm.dev, Paris. Corresponding author of the BB(5) paper.

2. **Shawn Ligocki** (sligocki.com) — Long-time Busy Beaver hunter since 2004 (initially with his father Terry Ligocki). Discovered the 10↑↑5 BB(6) bound in May 2022. Maintains extensive analysis blog and the `busy-beaver` GitHub repository. Made a $1,000 bet with John Tromp that BB(7) > Graham's number will be proven within 10 years.

3. **Pavel Kropitz** — Discovered the 10↑↑15 BB(6) record held from May 2022 to June 2025. Also discovered the 2010 record. In May 2025, found BB(7) > 2{11}2{11}3 (Ackermann level). Core bbchallenge collaborator.

4. **mxdys** (pseudonymous, GitHub: ccz181078) — Current BB(6) champion discoverer (2↑↑↑5, June 2025). Maintains the BB(6) holdouts list (~1,212 machines as of Feb 2026). Developed the new Finite Automata Reduction (FAR) method that decided 113 of 1,534 holdouts.

5. **Maja Kądziołka** — Resolved Skelet #17, the hardest holdout in BB(5). Paper: arXiv:2407.02426.

6. **Katelyn Doucette** (katelyndoucette.com) — Discovered Shift Overflow Counters, a new class of TM behavior achieving extreme runtimes.

7. **Nick Drozd** (nickdrozd.github.io) — Major contributor to BB enumeration techniques, TNF implementation, and ZFC independence conjectures.

8. **Pascal Michel** — Historical expert; maintains the canonical "Busy Beaver Competitions" page since 2004 and comprehensive historical survey (HAL: hal-00396880).

9. **Scott Aaronson** (UT Austin) — Author of the landmark 2020 survey "The Busy Beaver Frontier." Proved (with Adam Yedidia) that BB(n) becomes independent of ZFC for some n. Active commentator and advocate.

10. **Georgi Georgiev (Skelet)** — Identified the famous "Skelet machines" (43 undecided 5-state machines) that were the hardest BB(5) holdouts.

### Organizations

- **The bbchallenge Collaboration** (bbchallenge.org) — The primary organized effort for systematic BB research
- **Google DeepMind** — Formalized the Antihydra conjecture in Lean for AI proof attempts (formal-conjectures repository)

## 5. Key Algorithmic Approaches

### TNF Enumeration (Tree Normal Form / Brady's Algorithm)

Introduced by Allen Brady in his 1964 PhD dissertation, TNF reduces the search space by canonicalizing equivalent TMs. For 5-state, 2-symbol: the raw count of possible machines is enormous, but TNF reduces to 181,385,789 machines. The algorithm builds TMs incrementally, only assigning transition rules as they are first encountered during simulation, and prunes symmetric/equivalent branches. The convention **TNF-1RB** starts all machines with the first transition being "write 1, move Right, go to state B."

### Automated Deciders

Programs that classify TMs as HALT, NONHALT, or UNKNOWN. From the bbchallenge deciders paper (arXiv:2504.20563):

1. **Cyclers / Translated Cyclers** — Detect when a TM enters a repeating cycle (possibly shifting along the tape)
2. **Backward Reasoning** — Prove non-halting by showing no configuration leads to the halt state
3. **CTL (Closed Tape Language)** — Prove non-halting by showing the reachable tape configurations form a closed set under the transition function
4. **Finite Automata Reduction (FAR)** — Model tape contents as regular languages; prove non-halting via finite automata closure. mxdys's enhanced FAR variant (2025) is the current state-of-the-art
5. **MITMWFAR (Meet-In-The-Middle With FAR)** — Developed by Iijil; bidirectional search + FAR
6. **Inductive Rules / Bouncers** — Detect recurring patterns, prove counters grow unboundedly

### Acceleration Techniques for Simulation

1. **Macro Machines** — Group consecutive tape cells into "macro symbols" (blocks of 2-4 cells) and simulate at a higher level
2. **Collatz-level acceleration** — For Collatz-like machines, prove inductive rules and evaluate modular arithmetic to skip iterations
3. **Shift Overflow Counters** — Identify binary counter behavior; overflow events create exponential jumps enabling tetrational-scale simulation
4. **Run-Length Encoding (RLE)** — Compress tape representation for machines that produce long runs of identical symbols
5. **Proof-based verification** — For machines exceeding simulation capacity, algebraic proofs replace step-by-step simulation

## 6. The BB(6) Landscape in 2025-2026

### The Antihydra Problem

Discovered in June 2024, the **Antihydra** (`1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA`) is a 6-state "Cryptid" machine whose halting depends on a Collatz-like conjecture. This proved that **BB(6) is Hard** — determining BB(6) requires resolving at least one Collatz-type open problem. Google DeepMind formalized the Antihydra in Lean as a benchmark for AI theorem proving.

### Current Holdouts

As of February 2026, approximately **1,212 undecided 6-state machines** remain from the bbchallenge enumeration. All have been simulated to at least 10^13 steps without halting. Several are identified as potential Cryptids whose halting may be independent of ZFC.

### Key Open Questions

1. Can all ~1,212 holdouts be decided, or does BB(6) hit ZFC independence?
2. Is the Antihydra Collatz-like problem solvable?
3. Does BB(6) exceed Graham's number? (Current bound 2↑↑↑5 is far below Graham's number)
4. Is BB(6) independent of ZFC? (Scott Aaronson considers this plausible)

### Implications for Our Research

The evolution from BB(6) > 10^36,534 (2010 record) to BB(6) > 2↑↑↑5 (2025 record) means that naive simulation is no longer viable for verification of champion machines. Modern BB(6) research requires:
- Algebraic proof of TM behavior rather than step-by-step simulation
- Sophisticated acceleration techniques (macro machines, shift overflow counters)
- Formal verification in proof assistants (Coq/Rocq, Lean)
- Collaborative systematic classification of the holdout machines

Our research will focus on understanding and reproducing these techniques, exploring the search landscape with novel heuristics, and potentially discovering interesting machines in under-explored subspaces of the 6-state TM space.

## 7. Key Resources

| Resource | URL |
|----------|-----|
| bbchallenge.org | https://bbchallenge.org |
| BB(6) wiki | https://wiki.bbchallenge.org/wiki/BB(6) |
| BB(5) paper | https://arxiv.org/abs/2509.12337 |
| Deciders paper | https://arxiv.org/abs/2504.20563 |
| Aaronson's BB(6) blog post | https://scottaaronson.blog/?p=8972 |
| Ligocki's BB analysis | https://www.sligocki.com/2022/06/21/bb-6-2-t15.html |
| mxdys Rocq proofs | https://github.com/ccz181078/busycoq/tree/BB6 |
| Pascal Michel's records | https://bbchallenge.org/~pascal.michel/bbc |
| Quanta Magazine feature | https://www.quantamagazine.org/busy-beaver-hunters-reach-numbers-that-overwhelm-ordinary-math-20250822/ |
| DeepMind Antihydra | https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Other/BusyBeaverAntihydra.lean |
| Aaronson's BB Frontier | https://www.scottaaronson.com/papers/bb.pdf |
