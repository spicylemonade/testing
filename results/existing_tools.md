# Existing BB Search Tools and Repositories

## 1. bbchallenge.org Seed Database & Platform

- **URL**: https://github.com/bbchallenge
- **Language**: Go (seed generator), Rust/Python/Go (deciders), HTML (frontend)
- **Approach**: Systematic enumeration of all n-state TMs in TNF, followed by automated deciders that classify each as HALT/NONHALT/UNKNOWN
- **Key Components**:
  - `bbchallenge-seed` (Go): Generates the initial seed database of undecided 5-state TMs (88,664,064 machines)
  - `bbchallenge-deciders` (Jupyter/Rust/Python/Go): Programs that decide halting/non-halting for specific TM families (Cyclers, CTL, FAR, Bouncers, etc.)
  - `bbchallenge-proofs` (TeX): Mathematical proofs backing the deciders
  - `bbchallenge-py` (Python/Jupyter): Python tooling for manipulating and visualizing TMs
  - `bbchallenge-undecided-index`: Tracks successive versions of the undecided machines index
  - `bbchallenge` (HTML): Web frontend for browsing and analyzing machines
- **Limitations**: Primarily focused on 5-state case for the proof. BB(6) seed database and deciders are works in progress. The seed generator for 6-state would produce an astronomically larger database.

## 2. Shawn Ligocki's busy-beaver

- **URL**: https://github.com/sligocki/busy-beaver
- **Language**: Python
- **Approach**: Configurable TM simulation with advanced acceleration techniques. Key tool: `Enumerate.py` which discovers champion machines using:
  - Macro machines (block symbols)
  - Proof systems (inductive rules for non-halting)
  - Translated cycler detection
  - Exponential linear rules
  - Configurable block sizes and multipliers
- **Key Features**: Discovered many BB(6) champion bounds. Supports both halting detection and sigma/step counting. Highly configurable for different search strategies.
- **Limitations**: Python-based, so not the fastest for raw enumeration. Designed for a single researcher's workflow, not distributed computing.

## 3. mxdys's Coq-BB5 / busycoq

- **URL**: https://github.com/ccz181078/Coq-BB5 and https://github.com/ccz181078/busycoq/tree/BB6
- **Language**: Coq/Rocq, some C++
- **Approach**: Formal verification of BB results in the Coq proof assistant. The BB6 branch contains partial proofs for the current BB(6) champion machine (2↑↑↑5).
- **Key Features**: Machine-checked proofs, FAR (Finite Automata Reduction) implementation that decided 113 holdout machines
- **Limitations**: Formal proofs are slow to develop. The BB(6) work is still partial.

## 4. FransFaase's SymbolicTM

- **URL**: https://github.com/FransFaase/SymbolicTM
- **Language**: C/C++
- **Approach**: Symbolic Turing Machine analysis for Busy Beaver problems. Uses symbolic representations of tape contents to reason about TM behavior algebraically rather than through step-by-step simulation.
- **Key Features**: Can handle machines whose behavior is too complex for naive simulation. Focuses on understanding the algebraic structure of TM behavior.
- **Limitations**: Specialized tool, not a general-purpose enumerator.

## 5. bb-gauge (MostAwesomeDude)

- **URL**: https://github.com/mostawesomedude/bb-gauge
- **Language**: Python
- **Approach**: Gauging the difficulty of mathematical problems through Busy Beaver-style uncomputable functions. Constructs specific TMs that encode mathematical conjectures.
- **Key Features**: Connects BB values to independence from formal systems.
- **Limitations**: Not a search tool per se; more of an analysis/construction framework.

## 6. Nick Drozd's BB Tools

- **URL**: https://nickdrozd.github.io/ (blog with associated code)
- **Language**: Python
- **Approach**: TNF enumeration ("Brady's algorithm"), tree normal form generation, and systematic classification. Contributed to bbchallenge deciders.
- **Key Features**: Good documentation of TNF implementation details, including the canonical TNF-1RB convention.
- **Limitations**: Code is scattered across blog posts; not a single unified repository.

## 7. TM Simulator Libraries (Various)

Several standalone TM simulators exist across languages:
- **turbotm** (Heiner Marxen, C): High-performance TM simulator used in the original BB(5) champion discovery
- **Turing Machine Visualization Tools** on bbchallenge.org: Web-based step-through simulators for analyzing individual machines
- **Macro Machines** implementations in Ligocki's repo: Python classes for accelerated simulation

## Summary Comparison

| Tool | Language | Search | Decide | Accelerate | Verify | Active |
|------|----------|--------|--------|------------|--------|--------|
| bbchallenge suite | Go/Rust/Python | Yes | Yes | Partial | Coq | Yes |
| sligocki/busy-beaver | Python | Yes | Yes | Yes | No | Yes |
| ccz181078/Coq-BB5 | Coq/C++ | No | Yes | No | Yes | Yes |
| FransFaase/SymbolicTM | C/C++ | No | Partial | Symbolic | No | Moderate |
| bb-gauge | Python | No | No | No | No | Moderate |
| bbchallenge-py | Python | No | No | No | No | Low |
