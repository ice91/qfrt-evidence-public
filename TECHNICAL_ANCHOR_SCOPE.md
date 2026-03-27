# TECHNICAL_ANCHOR_SCOPE

This document defines the public boundary of the QFRT technical anchor repository.
It is intended for reviewers, collaborators, and integrators who need a stable,
portable evidence surface.

## 1) What this repository provides

This public repository provides a curated, review-facing technical package:

- **Curated artifacts**
  - Frozen, human-readable evidence outputs organized for inspection and audit.
- **Configs**
  - Public configuration snapshots needed to interpret exposed artifacts.
- **Summary tables**
  - Consolidated tables designed for reproducible reading and comparison.
- **Figure crosswalk**
  - Mapping between table/figure items and canonical artifact paths.
- **Public documentation**
  - Evidence interpretation notes, traceability guidance, and reviewer checklists.

Operationally, this repository is optimized for **read + verify + export**
workflows on repo-local paths.

## 2) What this repository does not provide

This public repository does not include:

- **Private core implementation**
  - Non-public core modules and protected implementation details.
- **Benchmark execution engine**
  - Full experiment orchestration stack and runtime-only pipelines.
- **Full run outputs**
  - Large raw run directories, intermediate scratch outputs, and machine-specific products.
- **Commercial/internal materials**
  - Non-public business materials, internal-only notes, and restricted operational content.

As a result, this repository should not be treated as a full execution workspace.

## 3) How to cite this repository as the QFRT technical anchor

When referencing QFRT evidence in external documents, cite this repository as the
**public technical anchor** and reference repo-local canonical paths.

Recommended citation practice:

1. Identify the evidence item (table, figure mapping, or reporting snapshot).
2. Cite the canonical repo-local path (for example under `artifacts/reporting/`).
3. Include the corresponding traceability/index references when provenance is needed.
4. Use immutable revision identifiers (commit/tag/release) in formal references.

Suggested wording:

> "Evidence is anchored in the QFRT public technical anchor repository, using
> curated artifacts and traceability metadata under repo-local canonical paths."

## 4) Data retained in private repositories

The following categories remain in private repositories and controlled execution
surfaces:

- Full benchmark orchestration code and execution automation.
- End-to-end run generation pipelines and high-volume raw outputs.
- Environment-specific integration details and deployment/runtime wiring.
- Restricted datasets, protected supplements, and non-public operational records.

Public evidence in this repository is designed to remain interpretable without
requiring direct access to those private systems.

## 5) Public-release posture

This scope is written for external release and long-term portability.
All public references should remain path-portable, reviewer-friendly, and
independent of machine-specific runtime assumptions.

