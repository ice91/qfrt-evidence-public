# QFRT Evidence Repository (Artifact-First)

This repository is a curated **public technical anchor** for QFRT evidence review.
It is intentionally focused on:

- frozen reporting tables,
- reproducibility-oriented traceability metadata,
- export utilities for assembling submission-facing bundles,
- documentation for interpreting curated artifacts.

It is **not** a full benchmark execution environment.

---

## Scope

Included:

- `docs/` evidence-facing documentation
- `artifacts/reporting/` curated reporting snapshots
- `artifacts/index/` run index metadata
- `artifacts/manifest.json` pointer metadata
- `scripts/export_*.py` export helpers

Not included in this repository:

- full benchmark execution stack
- large generated run directories
- environment-specific absolute paths

---

## Repository layout

- `docs/` — evidence interpretation docs and figure/table mapping notes
- `artifacts/` — frozen reporting and lightweight provenance metadata
- `scripts/` — export helpers for assembling review-facing bundles

---

## Usage model

Use this repo as a **read + export** surface:

1. read curated summaries from `artifacts/reporting/`
2. verify provenance via `artifacts/index/` and `artifacts/manifest.json`
3. use export scripts to produce compact reviewer-facing bundles

For full benchmark generation, use the corresponding execution workspace.

---

## Release policy notes

- Paths in this repo should remain repo-local and portable.
- Any unresolved artifact reference is marked explicitly as TODO/placeholder.
- This repository is released under the BSD 3-Clause License.
