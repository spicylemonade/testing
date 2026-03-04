# Information Bottleneck Approach to Chvatal-Sankoff Bounds

## Topic Context

The information bottleneck (IB) framework from Tishby et al. (1999) finds the optimal tradeoff
between compression and relevant information preservation. Applied to LCS:

- X, Y are independent random binary strings
- S = LCS(X,Y) is a "compressed" representation of their shared structure
- Information-theoretic limits on how much S can encode about X (or Y) constrain |S|/n = gamma_2

The deep connection here is to the **binary deletion channel**: if you send a binary string X
through a channel that deletes each bit independently with probability 1/2, the surviving bits
form a random subsequence. The LCS of X and Y is related to the longest message that could
survive independent deletion in both strings.

## Key Bound Derivation

If C_del(1/2) is the capacity of the binary deletion channel with deletion probability 1/2,
then the maximum rate at which information can be transmitted through the channel constrains
how long a common subsequence can be. Specifically:
gamma_2 <= 1 - H^{-1}(1 - 2*C_del(1/2))
where H^{-1} is the inverse binary entropy function.

## Implementation Backlog

1. [ ] Compute exact LCS distribution for n=1..15
2. [ ] Calculate mutual information quantities I(X; LCS(X,Y))
3. [ ] Derive explicit formula relating gamma_2 to C_del(1/2)
4. [ ] Use best known C_del(1/2) <= 0.4943 (Cheraghchi 2020)
5. [ ] Compute resulting upper bound on gamma_2
6. [ ] Compare with Lueker's 0.826280
7. [ ] Study achievability: can the bound be approached?
