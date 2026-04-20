# PUBLIC_RELEASE_NOTE

## First public release

This repository is the public QFRT technical anchor. It provides a curated
evidence surface for external review, including frozen reporting artifacts,
summary tables, traceability metadata, and supporting documentation for
interpreting the released materials.

This repository does not provide a full benchmark execution environment, full
raw output trees, or environment-specific operational wiring. It is intended as
a stable read, verify, and export surface for released evidence rather than a
complete generation workspace.

When citing QFRT evidence, cite this repository as the **QFRT public technical
anchor** and reference the canonical repo-local path for the relevant artifact,
table, figure mapping, or reporting snapshot. For formal references, include an
immutable revision identifier, preferably a tagged release or otherwise a pinned
commit.

The first public release represents the initial curated external release of the
QFRT evidence surface. It establishes the baseline public package for citation,
review, and traceability, with release-facing documentation and metadata aligned
to long-term public use.

For this release, the active public entry points are repo-local reporting paths
under `artifacts/reporting/`, including `summary_table.csv`,
`EXPERIMENT_ANALYSIS_TABLES.md`, `paper_runs/latest.txt`, and
`phase1_regime_boundary/latest.txt`. Run IDs in `artifacts/manifest.json` and
`artifacts/index/run_index.*` are provenance metadata; `bundle_ref://...`
values are not expected to resolve as local files in this repository.
The `latest.txt` files are navigation pointers within the cited repository
revision, not standalone immutable citation targets.
