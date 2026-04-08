# Phase D Implementation Log

## Files changed

- `README.md` - Added canonical public entry points and clarified that `bundle_ref://...` values are provenance labels, not local runtime paths.
- `PUBLIC_RELEASE_NOTE.md` - Added a concise release-facing statement of active repo-local reporting paths and provenance-only run metadata.
- `RELEASE_NOTES.md` - Added notes distinguishing active reporting paths, reporting `latest.txt` pointers, and provenance-only pack metadata.
- `TECHNICAL_ANCHOR_SCOPE.md` - Listed primary public reporting entry points and clarified how manifest, run index, and `latest.txt` references should be cited.
- `artifacts/README.md` - Corrected the directory description so omitted raw `packs/` roots are not presented as included public artifacts.
- `artifacts/reporting/README.md` - Added the active reporting entry points and clarified reporting `latest.txt` usage.
- `artifacts/reporting/paper_runs/paper_run__20260320-131447__e134d585/README.md` - Replaced execution-workspace regeneration guidance with public-anchor provenance guidance.
- `artifacts/reporting/phase1_regime_boundary/phase1_20260324T074328Z/README.md` - Marked `phase1_regime_boundary_out/...` source labels as provenance-only.
- `docs/ARTIFACT_TRACEABILITY.md` - Clarified repo-local reporting paths, manifest latest pack IDs, and `bundle_ref://...` provenance labels.
- `docs/EXPERIMENT_ANALYSIS.md` - Aligned source-of-truth wording with the top-level summary table, paper-run pointer, Phase I pointer, manifest, and run index.
- `docs/PAPER_FIGURES.md` - Clarified which latest pointer applies to assembled paper-run snapshots versus exploratory Phase I boundary material.
- `docs/REVIEWER_CHECKLIST.md` - Added checks for manifest/run-index provenance labels and reporting `latest.txt` pointers.

## Path assumptions kept intentionally

- Existing run IDs, generated timestamps, checksums, CSV/table contents, and figure artifacts were not changed.
- `bundle_ref://...` remains the compact provenance label format in `artifacts/index/run_index.csv` and `artifacts/index/run_index.jsonl`.
- `artifacts/reporting/paper_runs/latest.txt` remains the active pointer for the latest assembled paper-run reporting snapshot.
- `artifacts/reporting/phase1_regime_boundary/latest.txt` remains the active pointer for the latest exploratory Phase I boundary snapshot.

## Validation notes

- README, release notes, technical-anchor scope, traceability docs, and reviewer checklist now describe the same public-anchor story: repo-local reporting paths are active public surfaces; manifest and index entries are provenance metadata.
- No numerical results, run IDs, checksums, CSV contents, or generated table contents were edited.
