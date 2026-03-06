# Citation Audit

## Auditor Scope

- Audited artifacts: `results/problem_statement.md`, `results/literature/literature_snapshot.json`, `results/verification/novelty_report.md`, `results/verification/benchmark_report.md`, and `sources.bib`.
- Goal: confirm that every named baseline or prior-art comparator already used in the research narrative has a matching citation entry or an explicit rationale in the literature files.

## Coverage Check

| Comparator or source | Citation status | Evidence |
| --- | --- | --- |
| REBOUND | cited | `sources.bib` entry `rein2011` |
| TRACE | cited | `sources.bib` entry `lu2024` |
| JANUS | cited | `sources.bib` entry `rein2017` |
| poliastro | cited | `sources.bib` entry `rodrguez2022` |
| Orekit | cited | `sources.bib` entry `orekit2025` |
| PhET Gravity and Orbits | cited | `sources.bib` entry `phet2026` |
| Universe Sandbox | cited | `sources.bib` entry `universesandbox2025` |
| Wasmtime deterministic execution docs | cited | `sources.bib` entry `wasmtime2026` |
| WebAssembly numerics spec | cited | `sources.bib` entry `webassembly2026` |
| MIT two-body notes | cited | `sources.bib` entry `mitocw2008` |

## Auditor Verdict

- Decision: pass.
- Rationale: every named baseline or prior-art comparator already used in Phase 1 through Phase 4 has a matching entry in `sources.bib`.
- Required follow-up: when `results/analysis.md` is written, every major interpretive claim should cite at least one of these entries directly instead of relying on uncited narrative carry-over.
