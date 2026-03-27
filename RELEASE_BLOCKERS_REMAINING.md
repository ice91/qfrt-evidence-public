# RELEASE_BLOCKERS_REMAINING

This list captures remaining items that still need a follow-up sanitize pass.

## High priority blockers

1. `docs/EXPLAINER_PUBLIC.md`
   - still contains direct runtime command references (`run_*`, smoke targets).
2. `docs/PARAMS.json` and `artifacts/configs/PARAMS.json`
   - still include `PPA` and `Claim` wording.
3. `docs/PAPER_FIGURES_CONFIG_CORE.json` and `artifacts/configs/PAPER_FIGURES_CONFIG_CORE.json`
   - still reference `benchmark_suite/...` paths.

## Medium priority blockers

1. `scripts/collect_artifacts.py`
   - includes `_pack_out`, `run_aggr_*`, and runtime source assumptions.
2. `scripts/export_phase1_regime_boundary.py`
   - includes direct `run_*` source naming in docstring/comments.
3. `scripts/export_paper_summary.py`
   - includes `run_id`/`run_dir` rooted runtime assumptions in docs/comments.

## Notes

- This sanitize pass intentionally targeted public-facing docs + manifest/index/csv surfaces.
- No private repo, monolith code, core code, or tests were modified.
- Remaining blockers should be handled in a dedicated follow-up pass if full public release hardening is required.

