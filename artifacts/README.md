# Evidence Artifacts (Repo-level)

This directory is a canonical, submission-friendly public evidence entry point.

## Structure
- `reporting/`: curated paper-facing exported tables, figures, and latest snapshot pointers
- `index/`: compact pack provenance index (`run_index.csv`, `run_index.jsonl`)
- `configs/`, `env/`: reproducibility snapshots
- `manifest.json`: latest pack run IDs and index locations

Raw `packs/` run roots are not included in this public repository. Pack origins
are represented by `bundle_ref://...` provenance labels in `index/run_index.*`
and by run IDs in `manifest.json`.

## RUN_ID Format
`<pack>__<tag>__<YYYYMMDD-HHMMSS>__<gitsha8>__<cfg8>`
