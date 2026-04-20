# CURATED_PACK_ADDENDUM_PLAN_PRE_M3

## Goal

Define the smallest review-facing curation step that exposes
`init_sweep_pack` and `omega_fix_pack` alongside the current curated
`paper_runs` reporting surface without:

- rewriting execution artifacts,
- inventing results beyond current manifest/index evidence,
- implying paper-grade sufficiency,
- or making `qfrt-evidence-public` the execution owner.

This plan is based on the current repository structure and the stated context
that the PRE-M3 memo and dated evidence map already identify these packs as
execution-side evidence references. Those two files are not present in this
repository, so this plan anchors itself to the repo-local manifest/index and
reporting conventions already in place.

## Current Surface

The current review-facing reporting pattern is:

- `artifacts/reporting/paper_runs/latest.txt`
  - stable pointer to the latest assembled paper-run snapshot
- `artifacts/reporting/paper_runs/<paper_run_id>/`
  - `manifest.json`
  - `README.md`
  - copied summary/table CSVs
  - copied figure subsets
- `artifacts/manifest.json`
  - latest pack run IDs across the public evidence surface
- `artifacts/index/run_index.csv` and `artifacts/index/run_index.jsonl`
  - compact run-level provenance with `bundle_ref://...` labels

Observed current `paper_runs` manifest pattern:

- bundle-level identity: `schema_version`, `paper_run_id`, `generated_at`, `git_sha8`
- provenance policy: `source_path_policy`
- per-pack sources: `sources.<pack>.run_id`, `run_dir`, `src_csv`
- curated outputs: `summary_files`, `table_aliases`, `summary_to_table_map`
- optional figure reporting: `figure_counts`, `figure_roles`,
  `recommended_main_figures`, `recommended_appendix_figures`
- explicit absence handling: `missing_packs`

Observed public provenance already available for the two requested packs:

- `artifacts/manifest.json` includes latest run IDs for:
  - `init_sweep_pack`
  - `omega_fix_pack`
- `artifacts/index/run_index.*` includes indexed run entries for both packs with
  `bundle_ref://...` provenance labels

What is not present in the current public `paper_runs` bundle:

- curated summary CSVs for `init_sweep_pack`
- paper-facing table aliases for `init_sweep_pack`
- curated summary CSVs for `omega_fix_pack`
- paper-facing table aliases for `omega_fix_pack`
- curated figures copied into the current `paper_runs` snapshot

## Recommended Curation Shape

### Recommendation

Use a **sibling auxiliary addendum bundle**, not a rewrite of the current
`paper_runs` snapshot and not a promotion of these packs into the core
paper-results table set.

Recommended shape:

- `artifacts/reporting/paper_runs_addendum/latest.txt`
- `artifacts/reporting/paper_runs_addendum/<addendum_id>/`
  - `manifest.json`
  - `README.md`
  - optional `table_pack_index.csv`

Recommended bundle identity:

- `bundle_type: "paper_runs_curated_addendum"`
- `addendum_scope: "indexed_execution_side_pack_references"`

### Why this is the narrowest safe step

- It keeps the existing `paper_runs` surface intact as the current curated
  paper-facing bundle.
- It exposes the two packs in a review-visible location under
  `artifacts/reporting/`, which matches the existing public entry-point model.
- It relies only on already-public run IDs and run-index metadata.
- It avoids pretending that these packs already have curated tables or paper
  figures in this repository.
- It preserves the repository rule that execution ownership stays outside this
  public anchor.

### Why not extend the current `paper_runs` manifest directly

Directly adding these packs into the existing `paper_runs/<paper_run_id>/manifest.json`
would blur two different statuses:

- packs with copied curated tables/figures intended for paper-facing reading
- packs that are only indexed execution-side references

That ambiguity creates review risk. A sibling addendum is more conservative and
clearer.

## Proposed Addendum Contents

### `README.md`

The README should:

- state that the addendum is review-facing and citation-safe,
- state that it exposes indexed execution-side pack references only,
- point reviewers back to `artifacts/reporting/paper_runs/latest.txt` for the
  current curated paper-facing bundle,
- point reviewers to `artifacts/manifest.json` and `artifacts/index/run_index.*`
  for provenance verification,
- state that regeneration, reassembly, and interpretation of raw execution
  outputs remain outside this repository.

### `manifest.json`

The manifest should be minimal and explicit. It should not include invented
summary/table paths if no curated files exist for those packs.

Recommended fields:

- `schema_version`
- `addendum_id`
- `generated_at`
- `git_sha8`
- `bundle_type`
- `addendum_scope`
- `parent_reporting_surface`
  - `artifacts/reporting/paper_runs/latest.txt`
- `source_path_policy`
  - explicit statement that execution-source references are provenance-only
- `packs`
  - object keyed by pack name

For each of:

- `init_sweep_pack`
- `omega_fix_pack`

include:

- `status`
  - `indexed_public_reference_only`
- `run_id`
  - from `artifacts/manifest.json`
- `index_rows`
  - references to `artifacts/index/run_index.csv` and/or `run_index.jsonl`
- `bundle_ref`
  - `bundle_ref://init_sweep_pack` or `bundle_ref://omega_fix_pack`
- `reporting_exposure`
  - `manifest_index_only`
- `paper_run_integration_status`
  - `not_curated_into_core_paper_tables`
- `notes`
  - short reviewer-facing description such as
    "execution-side evidence reference; no curated summary/table copied here"

### Optional `table_pack_index.csv`

If one compact table is desired, keep it strictly administrative. Suggested
columns:

- `pack`
- `status`
- `run_id`
- `bundle_ref`
- `index_csv`
- `index_jsonl`
- `reporting_exposure`
- `paper_run_integration_status`
- `notes`

This file should function as a navigation crosswalk only, not a result table.

## Minimum Required Metadata

Minimum required bundle fields for the addendum:

1. `schema_version`
2. `addendum_id`
3. `generated_at`
4. `git_sha8`
5. `bundle_type`
6. `addendum_scope`
7. `parent_reporting_surface`
8. `source_path_policy`
9. `packs.init_sweep_pack.run_id`
10. `packs.init_sweep_pack.bundle_ref`
11. `packs.init_sweep_pack.status`
12. `packs.init_sweep_pack.reporting_exposure`
13. `packs.omega_fix_pack.run_id`
14. `packs.omega_fix_pack.bundle_ref`
15. `packs.omega_fix_pack.status`
16. `packs.omega_fix_pack.reporting_exposure`

Minimum reviewer-readable README statements:

- this is an auxiliary addendum, not the core paper bundle
- these packs are exposed as indexed execution-side references only
- provenance is verified through `artifacts/manifest.json` and
  `artifacts/index/run_index.*`
- this repository is not the execution owner

## Explicit Non-Claims

The addendum should explicitly state all of the following:

- It does **not** claim that `init_sweep_pack` or `omega_fix_pack` are already
  curated into the current core `paper_runs` result tables.
- It does **not** claim that these packs are sufficient on their own for
  manuscript-grade evidence.
- It does **not** claim that raw execution outputs are present in this public
  repository.
- It does **not** claim that `bundle_ref://...` values resolve to local runtime
  directories.
- It does **not** claim that this repository can regenerate or validate the
  underlying execution workflows.
- It does **not** reopen bridge work, pack restructuring, or execution-side
  bundle redesign.
- It does **not** introduce new result summaries, figures, or conclusions not
  already present in public manifests/indexes.

## Conservative Implementation Sequence

1. Create `artifacts/reporting/paper_runs_addendum/<addendum_id>/manifest.json`.
2. Create a short `README.md` with the status and non-claims above.
3. Optionally add `table_pack_index.csv` as a navigation-only crosswalk.
4. Create/update `artifacts/reporting/paper_runs_addendum/latest.txt`.
5. Optionally add one auxiliary row to `artifacts/reporting/paper_artifact_map.csv`
   pointing to the new addendum pointer.

No execution artifacts should be copied or rewritten.

## What Remains Unproven After The Addendum

Even after this addendum, the following remain unproven within the public
review-facing surface:

- any pack-level scientific result claims for `init_sweep_pack`
- any paper-grade summary table content for `init_sweep_pack`
- any pack-level scientific result claims for `omega_fix_pack`
- any paper-grade summary table content for `omega_fix_pack`
- any figure-level recommendation status for either pack
- any statement that these packs are fully integrated into the current curated
  `paper_runs` reporting bundle
- any statement that public review materials are sufficient to reproduce or own
  the execution pipeline

## Recommended Decision

Adopt a **manifest-first auxiliary addendum** under
`artifacts/reporting/paper_runs_addendum/` and keep the current
`artifacts/reporting/paper_runs/` bundle unchanged.

This is the narrowest review-facing curation step that exposes
`init_sweep_pack` and `omega_fix_pack` without overclaiming what the public
anchor currently contains.
