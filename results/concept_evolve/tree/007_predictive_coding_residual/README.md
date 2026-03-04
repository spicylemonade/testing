# Predictive Coding Residual Decode

## Context

In neuroscience, the predictive coding framework (Rao & Ballard 1999) posits that the brain maintains an internal model that predicts incoming sensory signals. Only prediction errors are propagated up the hierarchy, reducing the computational load. This has a direct analogy to entropy coding: the most common symbols carry the least information (surprise).

## Cross-Domain Bridge

The neuroscience insight translates to decompression: if we can predict the most likely next symbol with high confidence, we can speculatively "decode" it with a simple comparison rather than a full table lookup. This is conceptually identical to how CPU branch predictors work - they speculate on the most likely execution path.

## Application to DEFLATE

In DEFLATE, the fast-path literal decode in dougallj's implementation is already a form of predictive coding: it assumes the next 2 symbols are both literals (the most common case for text data) and decodes them in a fast path without checking for match/end-of-block codes.

Extending this: for data with very skewed distributions (e.g., whitespace-heavy XML, null-padded binaries), we could predict specific symbols:
- XML: predict literal ' ' (space) or '<' 
- Binary: predict literal 0x00
- Text: predict literal ' ' or 'e'

## Implementation Backlog

- [ ] Profile DEFLATE symbol frequency distributions across file types
- [ ] Implement top-1 prediction fast path
- [ ] Measure branch prediction accuracy of the speculative check
- [ ] Compare against dougallj's 2-literal fast path approach
- [ ] Analyze when prediction helps vs hurts (skewed vs uniform distributions)
- [ ] Explore adaptive prediction that learns from recent symbols
