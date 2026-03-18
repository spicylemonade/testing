# Citation Audit

## Supported Final Position

The following final-position sentences are supported by the saved bibliography together with the repo artifacts:

- Arithmetic Kakeya remains anchored in the Katz-Tao / Green-Ruzsa / Cowen-Breen / Pohoata-Zakharov line, so this run should not be presented as a new theorem or reformulation.
- Tao (2025) is the relevant barrier note for bounded-slope / rational-complexity risk, and the surviving corridor controls stay in the tiny fixed-`X` corridor regime that triggers that warning.
- Bootstrap / critical CA, abelian-network, and local-decoder papers are relevant only as overlap checks; the final route failed to produce a positive differentiated mechanism against any of those lines.

Most positive and negative performance claims in the final package are experiment-backed rather than bibliography-backed. The bibliography supports the novelty guardrails and barrier framing, while the repo artifacts support the obstruction, score tables, ablations, and pivot decisions.

Relevant bibliography anchors in `sources.bib`:

- `katz1999`
- `green2017`
- `cowenbreen2020`
- `pohoata2024`
- `tao2025`
- `bond2013`, `bond2014`, `bond2015`
- `bollobas2014`, `hartarsky2018`
- `kubica2018`, `hemenway2013`
- `sipser1996`

## Wording To Avoid

- “We solved arithmetic Kakeya using cellular automata.”
- “The forcing process is a cellular automaton.”
- “This introduces a new arithmetic-Kakeya framework.”
- “The CA route improved exact scores over matched arithmetic baselines.”
- “Abelian-network invariants uncovered new forcing structure.”

These sentences are not supported by either the bibliography or the verified artifacts.

## Citation Gaps To Keep Explicit

- The final negative empirical claims come from repo artifacts, not external papers. They should be cited to the verification and Phase 4 result files, not to the bibliography.
- The `1.675` threshold is a task-level benchmark target, not a literature claim.
- The surviving positive claim is only an operational benchmark/falsification workflow. That claim should always stay attached to the existing arithmetic-Kakeya and overlap-line citations above.

## Audit Verdict

The literature support is adequate for a narrow negative final position.

- Supported:
  - operational differentiation from the cited theorem/reformulation lines
  - explicit overlap checks against CA / abelian / decoder folklore
- Unsupported:
  - any positive novelty claim stronger than “exact corridor benchmark-and-falsification workflow”

Open risk:

- if the final writeup blurs repo-generated negative evidence with bibliographic theorem claims, it will overstate what the citations actually support.
