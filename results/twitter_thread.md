# BB(6) Search Campaign: Twitter Thread Draft

## Hype Tweet (One-liner)

We searched 1,000,000+ Turing machines for new BB(6) lower bounds. Best find: a single bit-flip in a known champion creates a machine that writes 80 ones in 2,452 steps. The real BB(6) champion? It outputs a number so large you need arrows to write it: > 2↑↑↑5.

---

## Thread

**1/8**
We just finished searching 1,000,000+ Turing machines for new BB(6) lower bound candidates.

BB(6) asks: what's the most 1s a halting 6-state Turing machine can write on a blank tape?

The answer is literally incomprehensible. Here's what we found (and didn't find).

**2/8**
The Busy Beaver function BB(n) is one of the craziest objects in math.

BB(1) = 1
BB(2) = 4
BB(3) = 6
BB(4) = 13
BB(5) = 4,098 (just proven in 2024!)
BB(6) > 2↑↑↑5

That last one means "2 pentation 5" — iterated tetration of 2. A number so large that even writing its number of digits takes more space than the observable universe.

**3/8**
We tried 4 search strategies:
- Random sampling (500K machines)
- Mutating known champions (1,296 machines)  
- "Breeding" champion substructures (125 machines)
- Feature-guided generation (500K machines)

All running on 20 cores with a C-accelerated simulator (60x faster than Python).

**4/8**
Our best find: a SINGLE direction flip in the Kropitz t15 champion creates a machine that writes 80 ones in 2,452 steps.

Original: ...0LE1RZ...
Mutant:   ...0RE1RZ...
          (L -> R, that's it)

Verified by both Python and C simulators. Cross-check: passed.

**5/8**
The most interesting result isn't the machine — it's the strategy comparison.

Mutation search explored only 0.13% of our machines but found the best results. Random search explored 500K machines and peaked at sigma=10.

Champion neighborhoods are RICH in interesting machines. The TM space has structure.

**6/8**
But let's be honest: sigma=80 vs the real BB(6) record of > 2↑↑↑5?

That's like comparing a grain of sand to... well, there's no metaphor. The gap isn't just astronomical. The NUMBER OF DIGITS in the record has more digits than atoms in the universe. Repeatedly.

**7/8**
Why? Because all known BB(6) champions work through algebraic mechanisms — Collatz-like rules, counter overflows — that AMPLIFY outputs exponentially at each step.

You can't find these by simulation. You need to recognize the math, prove it terminates, and compute the output symbolically.

**8/8**
What we learned:
1. Mutation search >> random search for BB exploration
2. Syntactic features (graph density, etc.) DON'T predict which machines are interesting  
3. Step-limited simulation is fundamentally insufficient for BB(6)
4. The path forward is algebraic analysis + formal verification

Full report, code, and a standalone verifier at [repo link].

Run `python3 verify.py` to check our best candidate yourself. It takes 0.01 seconds.
