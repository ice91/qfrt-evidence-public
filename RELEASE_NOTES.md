# RELEASE_NOTES

## Candidate Freeze (2026-03-27)

This candidate freeze packages the public evidence surface for QFRT technical review.

### Included in this freeze

- Artifact-first repository documentation
- Curated reporting artifacts and summary tables
- Public-safe supporting metadata
- Traceability/index metadata for provenance navigation
- Optional export-helper scripts with public-release framing

### Key preparation steps completed

- Public-facing wording harmonized across release documents
- Final keyword sweep for runtime-specific command strings
- Placeholder usage inventory for `TODO_PUBLIC_PLACEHOLDER://...`
- Placeholder interpretation policy documented in `PLACEHOLDER_POLICY.md`

### Notes

- This repository is a public technical anchor and curated evidence surface.
- It is not a full benchmark execution environment.
- Placeholder entries are intentional and governed by `PLACEHOLDER_POLICY.md`.
- Active public evidence should be read from repo-local paths under
  `artifacts/reporting/`; latest reporting pointers live at
  `artifacts/reporting/paper_runs/latest.txt` and
  `artifacts/reporting/phase1_regime_boundary/latest.txt`.
- `artifacts/manifest.json` and `artifacts/index/run_index.*` provide pack-level
  provenance metadata. `bundle_ref://...` entries identify provenance bundles
  and are not local runtime paths.
