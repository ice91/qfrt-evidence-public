# EVIDENCE_PUBLICATION_FREEZE_0515

## Purpose

This memo freezes the minimum public-anchor surface needed before **May 15,
2026** so `qfrt-evidence-public` no longer blocks paper-facing use.

The goal is publication-safe enough for citation and review use, not broader
curation expansion and not paper-grade completeness.

## Publication-Ready Enough Now

The repository is publication-ready enough now for paper-facing use when used as
a **public technical anchor** with the current assembled surfaces:

- `artifacts/reporting/summary_table.csv`
- `artifacts/reporting/EXPERIMENT_ANALYSIS_TABLES.md`
- `artifacts/reporting/paper_runs/latest.txt`
- `artifacts/reporting/phase1_regime_boundary/latest.txt`
- `artifacts/reporting/paper_runs_addendum/latest.txt`
- `artifacts/manifest.json`
- `artifacts/index/run_index.csv`
- `artifacts/index/run_index.jsonl`
- scope/traceability docs that explain the public-boundary rules

This is sufficient for:

- citing repo-local canonical paths,
- pointing reviewers to the assembled paper-facing reporting bundle,
- pointing reviewers to the exploratory Phase I bundle where relevant,
- exposing `init_sweep_pack` and `omega_fix_pack` as indexed execution-side
  references only,
- and verifying lightweight provenance through manifest/index metadata.

## Intentionally Deferred Until After May 15, 2026

The following are intentionally deferred:

- broader curation or reorganization of reporting surfaces
- new reporting bundles beyond what is already assembled
- promotion of addendum-only packs into core `paper_runs` result tables
- checksum or crosswalk cleanup that is not required for current citation use
- broader documentation polish
- execution-workspace reconciliation or regeneration work
- any attempt to make this repo look like a full execution owner

## Canonical Surfaces To Cite Or Use

Before May 15, 2026, the canonical surfaces are:

- `artifacts/reporting/EXPERIMENT_ANALYSIS_TABLES.md`
  - curated paper-facing table snapshot
- `artifacts/reporting/paper_runs/latest.txt`
  - pointer to the latest assembled core paper-run reporting snapshot
- `artifacts/reporting/phase1_regime_boundary/latest.txt`
  - pointer to the exploratory Phase I boundary snapshot
- `artifacts/reporting/paper_runs_addendum/latest.txt`
  - pointer to the review-facing addendum for indexed execution-side references
- `artifacts/manifest.json`
  - latest public pack run IDs
- `artifacts/index/run_index.csv` and `artifacts/index/run_index.jsonl`
  - compact provenance metadata

Use repo-local paths plus a pinned revision/tag when formal citation is needed.

## Do Not Edit Again Before May 15, 2026 Unless Critical

Treat the following as frozen unless a change is needed to fix a real blocking
issue, a citation-safety problem, or an incorrect public reference:

- `README.md`
- `TECHNICAL_ANCHOR_SCOPE.md`
- `artifacts/reporting/README.md`
- `artifacts/reporting/EXPERIMENT_ANALYSIS_TABLES.md`
- `artifacts/reporting/paper_runs/`
- `artifacts/reporting/phase1_regime_boundary/`
- `artifacts/reporting/paper_runs_addendum/`
- `artifacts/manifest.json`
- `artifacts/index/run_index.csv`
- `artifacts/index/run_index.jsonl`

Critical means one of:

- wrong canonical pointer
- broken repo-local citation path
- misleading public ownership claim
- incorrect provenance reference

Not critical:

- style polish
- wording improvements
- optional cleanup
- extra summary convenience work
- broader curation ideas

## Maintainer Rule

If it is already citation-safe, review-readable, and non-blocking for the paper,
**stop editing it and move on**.
