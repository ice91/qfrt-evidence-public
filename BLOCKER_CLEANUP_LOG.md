# BLOCKER_CLEANUP_LOG

Date: 2026-03-27  
Pass: targeted blocker cleanup (from `RELEASE_BLOCKERS_REMAINING.md`)

## Scope handled

Processed only blocker-listed files:

- `docs/EXPLAINER_PUBLIC.md`
- `docs/PARAMS.json`
- `artifacts/configs/PARAMS.json`
- `docs/PAPER_FIGURES_CONFIG_CORE.json`
- `artifacts/configs/PAPER_FIGURES_CONFIG_CORE.json`
- `scripts/collect_artifacts.py`
- `scripts/export_phase1_regime_boundary.py`
- `scripts/export_paper_summary.py`

## Actions taken

1. `docs/EXPLAINER_PUBLIC.md`
   - Replaced remaining runtime command references (`make`, `run_*`, `verify` script, `*_out`) with artifact-first wording.
2. `docs/PARAMS.json` + `artifacts/configs/PARAMS.json`
   - Removed PPA/Claim wording.
   - Renamed `primary_pdf`/`secondary_pdf` to public-neutral `primary_reference`/`secondary_reference`.
   - Kept technical semantics, switched to release-safe phrasing.
3. `docs/PAPER_FIGURES_CONFIG_CORE.json` + `artifacts/configs/PAPER_FIGURES_CONFIG_CORE.json`
   - Removed direct `benchmark_suite/...` dependencies.
   - Replaced with repo-local TODO placeholders using `TODO_PUBLIC_PLACEHOLDER://...`.
4. scripts (`collect_artifacts.py`, `export_phase1_regime_boundary.py`, `export_paper_summary.py`)
   - Added top-level public-release notes declaring them optional export helpers, not full execution pipelines.
   - For phase1 exporter docstring, removed direct `run_*` source naming in top comments.

## Out-of-scope (not modified)

- monolith / private repos / core code / tests
- runtime logic and algorithm behavior
- non-blocker files not listed in `RELEASE_BLOCKERS_REMAINING.md`

