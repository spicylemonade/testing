# Ostrowski Synchronized Subsequence Search

## Topic context
Quadratic irrationals already admit synchronized descriptions of Beatty membership via Ostrowski numeration. This card turns that machinery into a search engine for hidden homogeneous linear recurrences inside floor(n*r) by treating both the selector n_k and the recurrence witness as automata-readable objects.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Fix a quadratic irrational r. Search for d >= 1, integers c_0,...,c_d with c_d != 0, and an increasing selector n_0 < n_1 < ... such that y_k = floor(r*n_k) and sum_{i=0}^d c_i*y_{k+i} = 0 for all k >= K. Encode (k,n_k,y_k) in Ostrowski numeration so the relation y = floor(r*n) and monotonicity of the selector are recognized by finite automata.

## Cross-domain analogies
- Use Ostrowski digits as a hardware clock for candidate subsequences.
- Treat the Beatty sequence as a synchronized stream and the recurrence as a regular-language invariant.
- Turn continued fractions into a compiler target for recurrence witnesses.

## Novel move
The new step is not merely deciding Beatty membership or first-order Beatty properties; it uses synchronized numeration as a witness generator for exact LRS subsequences.

## Why this is not just a reimplementation
Existing automata papers stop at definability and decidability of Beatty or Sturmian relations. This proposal adds a recurrence-template search layer that outputs candidate subsequences and orders, not just yes or no membership answers.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Use Walnut or Pecan style automata over Ostrowski representations of a quadratic r. Enumerate recurrence orders d <= 4 and coefficient boxes |c_i| <= C, encode selector families by transducers, and ask for an accepting run that certifies an exact recurrence.
2. Run the first experiment: Start with r in {phi, sqrt(2), 1+sqrt(2), (3+sqrt(5))/2}. For each r, search selectors of automaton size <= 6 and recurrence order <= 4, then record the smallest exact witness or a proof that the tested template family fails.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Beatty Sequences for a Quadratic Irrational: Decidability and Applications (74492951ce0e23319ffde058fc107cefc4488d0e, 2024, arXiv.org): Shows that Beatty relations for quadratic irrationals are synchronized in Ostrowski numeration.
- Ostrowski-automatic sequences: Theory and applications (60d51405e92dd39f0836d04dbbe88f5904b094b3, 2021, Theoretical Computer Science): Provides the automatic-sequence infrastructure needed to encode selector and value relations.
- Decidability for Sturmian words (9db8fdff7bca15077834c62d6051340e5e06180b, 2021, Annual Conference for Computer Science Logic): Supplies the decidability template for Sturmian and Ostrowski-automatic settings.
- Sturmian numeration systems and decompositions to palindromes (31a0025e468f7d7c604ea3ca3227a102aa00ff87, 2017, European Journal of Combinatorics): Connects richer Ostrowski-style numeration to local symbolic structure that can guide selector design.

