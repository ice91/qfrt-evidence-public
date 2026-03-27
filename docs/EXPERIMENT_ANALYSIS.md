# Experiment Analysis (Evidence-First View)

This document explains how to read curated summaries in this repository.

## What this document does

- describes evidence axes used by reporting tables,
- clarifies interpretation boundaries,
- links evidence statements to curated table surfaces.

## Evidence axes

1. Stability under irregular observations
2. Two-layer gain summary
3. Low-z onset interval summary
4. SNR robustness summary
5. Mask robustness summary (validated runs only)
6. Mechanism-oriented diagnostics (if present in curated tables)

## Interpretation boundaries

- Interval statements should remain interval statements.
- Robustness language should be phrased as "robust but attenuating" where applicable.
- If a required source is unavailable in the public evidence surface,
  it should be marked as TODO/placeholder instead of inferred.

## Source of truth in this repo

- `artifacts/reporting/` for curated reporting tables
- `artifacts/index/` for compact provenance metadata
- `artifacts/manifest.json` for latest pointers

## Public-surface constraint

This document intentionally avoids requiring full execution-stack details.

