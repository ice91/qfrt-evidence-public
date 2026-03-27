# Evidence Artifacts (Repo-level)

This directory is a canonical, submission-friendly Evidence Pack entry point.

## Structure
- `packs/`: per-pack, versioned runs (`RUN_ID/`), each with `manifest.json` + `checksums.sha256`
- `index/`: global run index (`run_index.csv`, `run_index.jsonl`)
- `configs/`, `env/`: reproducibility snapshots
- `reporting/`: paper-facing exported tables (e.g., EXPERIMENT_ANALYSIS_TABLES.md)

## RUN_ID Format
`<pack>__<tag>__<YYYYMMDD-HHMMSS>__<gitsha8>__<cfg8>`

