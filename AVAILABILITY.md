# AVAILABILITY

## Public repository role

This repository is publicly structured as a QFRT technical anchor, providing
curated artifacts, reporting summaries, traceability metadata, and supporting
documentation for external technical review.

## What is available here

- `docs/` public-facing evidence documentation
- `artifacts/reporting/` curated reporting outputs
- `artifacts/index/` lightweight provenance index metadata
- `artifacts/manifest.json` top-level pointer metadata
- `scripts/` optional export helpers for assembling review-facing bundles

## What is not included here

- full benchmark execution pipeline
- full raw output trees
- operational materials not included in this public evidence surface

## Usage expectation

Consumers should use repo-local artifact paths and traceability metadata as the
primary reference surface for citation, review, and cross-checking.

For formal citation, use a tagged release or pinned commit. `latest.txt` files
are convenience pointers within a checked-out revision; they are not themselves
immutable citation targets.
