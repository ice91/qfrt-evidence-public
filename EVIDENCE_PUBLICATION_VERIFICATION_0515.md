# EVIDENCE_PUBLICATION_VERIFICATION_0515

## Result

Verification date: 2026-04-20

Pre-5/15 publication-freeze verification was run against the canonical surfaces
defined in `EVIDENCE_PUBLICATION_FREEZE_0515.md`.

Status: **GO**

## Verified Canonical Surfaces

The following canonical public-anchor paths exist and resolve repo-locally:

- `artifacts/reporting/summary_table.csv`
- `artifacts/reporting/EXPERIMENT_ANALYSIS_TABLES.md`
- `artifacts/reporting/paper_runs/latest.txt`
- `artifacts/reporting/phase1_regime_boundary/latest.txt`
- `artifacts/reporting/paper_runs_addendum/latest.txt`
- `artifacts/manifest.json`
- `artifacts/index/run_index.csv`
- `artifacts/index/run_index.jsonl`

The following `latest.txt` pointers resolve to existing snapshot directories:

- `artifacts/reporting/paper_runs/latest.txt`
  - `artifacts/reporting/paper_runs/paper_run__20260320-131447__e134d585`
- `artifacts/reporting/phase1_regime_boundary/latest.txt`
  - `artifacts/reporting/phase1_regime_boundary/phase1_20260324T074328Z`
- `artifacts/reporting/paper_runs_addendum/latest.txt`
  - `artifacts/reporting/paper_runs_addendum/paper_runs_addendum__20260420-102254__a12bd8ff`

## Critical Issues Fixed

One critical consistency issue was fixed:

- The freeze memo names `artifacts/reporting/paper_runs_addendum/latest.txt` as
  canonical, but the main public entry-point docs did not yet list it.

Minimal fixes were applied to:

- `README.md`
- `TECHNICAL_ANCHOR_SCOPE.md`
- `artifacts/reporting/README.md`

These edits aligned the public entry-point lists without broadening curation or
changing any reporting bundle contents.

## Provenance And Ownership Check

Verified:

- `artifacts/manifest.json` points to repo-local index files
- `artifacts/index/run_index.csv` and `artifacts/index/run_index.jsonl` are
  internally consistent for the exposed pack rows
- `bundle_ref://...` values are described as provenance labels, not local paths
- public docs continue to state that `qfrt-evidence-public` is not the execution
  owner

## Deferred

Intentionally deferred and not required for pre-5/15 GO:

- broader curation changes
- new bundles
- checksum expansion
- optional crosswalk cleanup
- non-critical wording polish
- execution-side regeneration or reconciliation work
