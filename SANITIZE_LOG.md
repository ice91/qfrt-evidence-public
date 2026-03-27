# SANITIZE_LOG

Date: 2026-03-27  
Mode: sanitize pass (public-facing docs + manifest/index/csv only)

## Scope applied

Updated files (sanitized):

- `README.md`
- `README_zh-TW.md`
- `docs/ARTIFACT_TRACEABILITY.md`
- `docs/EXPERIMENT_ANALYSIS.md`
- `docs/PAPER_FIGURES.md`
- `docs/REVIEWER_CHECKLIST.md`
- `artifacts/manifest.json`
- `artifacts/index/run_index.csv`
- `artifacts/index/run_index.jsonl`
- `artifacts/reporting/README.md`
- `artifacts/reporting/paper_artifact_map.csv`

## What was sanitized

1. Rewritten docs to artifact-first/evidence-first framing.
2. Removed direct references to monolith runtime assumptions in rewritten docs.
3. Neutralized sensitive wording where found in rewritten docs.
4. Replaced `src_dir` runtime folder names in index files with `bundle_ref://...` placeholders.
5. Removed non-anchor `run_aggr_*` entries from root artifact manifest.
6. Simplified paper artifact map to public evidence-facing entries with repo-local paths.

## Not changed by design

- Python runtime/export scripts were not edited in this pass.
- Non-target docs/configs not listed in the request were not rewritten.
- No execution outputs were regenerated.

