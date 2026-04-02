# TECHNICAL_ANCHOR_SCOPE

This document defines the public boundary of the QFRT technical anchor repository.
It is intended for reviewers, collaborators, and integrators who need a stable,
portable evidence surface.

## 1) What this repository provides

This public repository provides a curated, review-facing evidence package:

- **Curated artifacts**
  - Frozen, human-readable evidence outputs organized for inspection and audit.
- **Supporting metadata**
  - Public metadata needed to interpret exposed artifacts.
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

- **Execution materials**
  - Additional implementation materials and full benchmark-generation workflows.
- **Full run outputs**
  - Large raw run directories, intermediate scratch outputs, and machine-specific products.
- **Additional operational materials**
  - Supplemental operational notes and restricted release materials.

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

## 4) Materials not included in this repository

The following categories are outside the scope of this repository:

- Full benchmark generation and execution automation.
- High-volume raw outputs and intermediate scratch products.
- Environment-specific integration details and deployment wiring.
- Restricted datasets, protected supplements, and operational records.

Public evidence in this repository is designed to remain interpretable without
requiring access to those additional materials.

## 5) Public-release posture

This scope is written for external release and long-term portability.
All public references should remain path-portable, reviewer-friendly, and
independent of machine-specific runtime assumptions.
