# Reporting Surface (Public Evidence)

This directory contains submission-facing curated reporting snapshots.
It is intended as a compact review entry point.

## Start here

- `summary_table.csv`
- `EXPERIMENT_ANALYSIS_TABLES.md`
- `paper_artifact_map.csv`
- `paper_runs/latest.txt`
- `phase1_regime_boundary/latest.txt`
- `paper_runs_addendum/latest.txt`

## Provenance in this public surface

- `../index/run_index.csv` for compact run metadata
- `../manifest.json` for latest pointers
- `paper_runs/latest.txt` for the latest assembled paper-run reporting snapshot
- `phase1_regime_boundary/latest.txt` for the latest exploratory Phase I boundary snapshot
- `paper_runs_addendum/latest.txt` for the latest review-facing addendum exposing indexed execution-side pack references

## Path policy

All references in this public surface should remain repo-local.
If a runtime source root is unavailable in this repository, it should be
represented with a neutral placeholder or provenance label rather than an
environment-specific path.
