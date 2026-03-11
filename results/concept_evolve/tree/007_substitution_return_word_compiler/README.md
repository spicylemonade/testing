# Substitution Return Word Compiler

## Topic context
The first-difference word of a Beatty sequence is mechanical, and for bounded-type slopes it is linearly recurrent as a word even when the arithmetic values are not obviously recurrent. This card compiles return words, substitution blocks, and their abelianized counts into candidate cumulative-sum subsequences whose values may fall onto a one-dimensional recurrence eigenspace.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Let Delta_n = floor((n+1)*r) - floor(n*r). Build the return-word system on the mechanical word Delta. For selected concatenation blocks w_k, define y_k as the cumulative sum up to the end of w_k. If the abelianization vectors of w_k evolve by a primitive substitution matrix M and project to a one-dimensional eigenspace, then y_k may obey a homogeneous LRS.

## Cross-domain analogies
- Compile a symbolic grammar into arithmetic totals.
- Turn return words into macro-instructions whose cumulative cost is recurrent.
- Use substitution matrices as transfer functions from words to values.

## Novel move
The bridge is from symbolic linear recurrence of the difference word to arithmetic linear recurrence of cumulative Beatty values.

## Why this is not just a reimplementation
Prior Sturmian and substitution papers analyze word structure, numeration, or complementary sequences. This card compiles those objects into candidate LRS subsequences of numeric Beatty values.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Compute return words for rational approximants of the slope, estimate the incidence matrix, and search for block families whose prefix-sum projections satisfy a fixed companion matrix. Validate by reconstructing the corresponding indices n_k in the Beatty sequence.
2. Run the first experiment: Test the Fibonacci and silver-ratio cases first, then non-quadratic bounded-type slopes. Measure whether exact recurrences survive when return-word blocks are grown by substitution depth.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Generalized Beatty sequences and complementary triples (99423440cb26736fac8589d091008d2118a1bcc0, 2018, Moscow Journal of Combinatorics and Number Theory): Shows Beatty identities built from compositional and substitution-like structure.
- Sturmian numeration systems and decompositions to palindromes (31a0025e468f7d7c604ea3ca3227a102aa00ff87, 2017, European Journal of Combinatorics): Uses extended Sturmian numeration to reflect local symbolic structure.
- Substitution Invariant Sturmian Words and Binary Trees (3c63b09bb62adda5ad09d0abc336d0b0d24301e7, 2017, Integers): Gives substitution-invariant Sturmian families that can anchor return-word compilers.
- The Frobenius problem for homomorphic embeddings of languages into the integers (114499cc4322a1eef8e70d903ebc6856df47f334, 2017, Theoretical Computer Science): Connects language embeddings into integers, providing an arithmetic image of symbolic words.

