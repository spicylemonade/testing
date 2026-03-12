# Concept: reverse_leakage_vote_or

- Rank: 4
- Description: Exploit leakage and subthreshold current signatures across startup OR-ing devices to vote on which source is truly sourcing energy versus being back-driven, then gate only the voted source into the startup path.
- Key mechanism: Matched leakage windows around OR-ing FETs can turn unavoidable device leakage into a direction detector.
- Predicted failure mode: Leakage signatures are too process- and temperature-sensitive to be robust.

## Dependencies
- startup OR-ing FETs
- leakage sample capacitors
- vote latch

## First Experiment
- Run polarity mismatch and source collapse cases to see whether the vote suppresses wrong-way startup events better than a fixed ideal-diode path.

## Novelty Guard
- Interesting only if it avoids explicit comparator power and still predicts back-drive direction reliably enough to matter.

## Closest Overlap
- Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (0fd82792)
- A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers (6022e537)
