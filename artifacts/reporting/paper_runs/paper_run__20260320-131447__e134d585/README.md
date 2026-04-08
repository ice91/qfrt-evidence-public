# Paper Run Summary

Generated:     2026-03-20T13:14:47
PAPER_RUN_ID:  `paper_run__20260320-131447__e134d585`
Git SHA-8:     `e134d585`

## Summary / table files

Each pack produces two files (same content, two naming conventions):

- `summary_baseline.csv` / `table_main_baseline.csv` — baseline_pack  (run_id: `baseline_pack__main__20260320-131433__e134d585__e3c71b41`)
- `summary_stress.csv` / `table_stress_missing.csv` — stress_sweep  (run_id: `stress_sweep__main__20260320-131434__e134d585__e3c71b41`)
- `summary_n_sweep.csv` / `table_n_scaling.csv` — n_sweep  (run_id: `n_sweep__main__20260320-131434__e134d585__e3c71b41`)
- `summary_coupling.csv` / `table_coupling.csv` — coupling_pack  (run_id: `coupling_pack__main__20260320-131434__e134d585__e3c71b41`)

## Figures

Key figures are copied into `figures/<pack_name>/`.
Main-manuscript figures: see `manifest.json` → `recommended_main_figures`.
Appendix/supplementary: see `manifest.json` → `recommended_appendix_figures`.

## Traceability

- This directory is the read-only public assembled paper-run reporting snapshot.
- Source pack run IDs are listed above and in `manifest.json`; their raw pack
  roots are provenance-only origins and are not included as local
  `artifacts/packs/<pack>/<RUN_ID>/` directories in this public repository.
- For pack-level provenance, use `../../../index/run_index.csv` and
  `../../../manifest.json`.
- Reassembly and experiment regeneration belong to the execution workspace, not
  this public technical anchor.
