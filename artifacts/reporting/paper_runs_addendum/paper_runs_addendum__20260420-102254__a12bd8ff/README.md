# Paper Runs Addendum

Generated:     2026-04-20T10:22:58+0800
ADDENDUM_ID:   `paper_runs_addendum__20260420-102254__a12bd8ff`
Git SHA-8:     `a12bd8ff`

## Status

This directory is a read-only, review-facing, citation-safe addendum to the
current curated `paper_runs` reporting surface.

It exposes `init_sweep_pack` and `omega_fix_pack` as indexed execution-side
references only. It does not change the existing core paper bundle under
`artifacts/reporting/paper_runs/`.

## What Is Included

- `manifest.json`
  - addendum identity, parent reporting pointer, provenance sources, pack-level
    indexed reference metadata, and explicit non-claims
- `table_pack_index.csv`
  - navigation-only crosswalk for the two indexed packs

For the current curated paper-facing reporting bundle, use:

- `artifacts/reporting/paper_runs/latest.txt`

For provenance verification, use:

- `artifacts/manifest.json`
- `artifacts/index/run_index.csv`
- `artifacts/index/run_index.jsonl`

## Review Use

Use this addendum to confirm that:

- `init_sweep_pack` has a public latest run ID and indexed bundle reference
- `omega_fix_pack` has a public latest run ID and indexed bundle reference
- both packs are exposed to reviewers in a citation-safe reporting location

This addendum is administrative and traceability-oriented. It is not a result
bundle and does not copy execution outputs into this repository.

## Non-Claims

- This addendum does not claim that `init_sweep_pack` is curated into the core
  `paper_runs` result tables.
- This addendum does not claim that `omega_fix_pack` is curated into the core
  `paper_runs` result tables.
- This addendum does not claim manuscript-grade sufficiency for either pack.
- This addendum does not claim that raw execution outputs are present in this
  public repository.
- This addendum does not claim that `bundle_ref://...` values resolve to local
  runtime directories.
- This addendum does not claim that `qfrt-evidence-public` can regenerate,
  validate, or own the underlying execution workflows.
- This addendum does not introduce new result summaries, figures, or scientific
  conclusions beyond already-public manifest/index metadata.
- This addendum does not reopen bridge work, execution-side restructuring, or
  core `paper_runs` bundle redesign.

## Ownership Boundary

`qfrt-evidence-public` remains a public technical anchor for read, verify, and
citation-safe reporting on repo-local paths. It is not the execution owner.
Execution-side reassembly, regeneration, and workflow validation remain outside
this repository.
