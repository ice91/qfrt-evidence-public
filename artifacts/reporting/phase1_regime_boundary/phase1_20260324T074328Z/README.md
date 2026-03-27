# Phase I Regime-Boundary Bundle

**RUN_ID**: phase1_20260324T074328Z  
**Generated (UTC)**: 2026-03-24T07:43:28Z

---

## ⚠️ Status

This is an **EXPLORATORY Phase I bundle**, NOT a formal paper artifact.  
It is produced by `scripts/export_phase1_regime_boundary.py` and must be
interpreted under the following constraints:

- **Current-init-policy**: θ_init is derived from `theta_init_from_true()` +
  PARAMS.json offset. The `z_override` changes `theta_true.z` only;
  estimator initialisation is NOT altered.
- **Headline method**: `P0_OGTR_CF_INIT`
- **Reference method**: `BL_OGTR_CF`
- **Scope**: Phase I boundary analysis only. For formal paper experiments,
  see `artifacts/reporting/paper_runs/` produced by the separate
  `paper_experiments` pipeline.

---

## Core Phase I Findings: Two-Layer Gain Structure

### 1. `material_rmse_gain` — General Refinement Gain
- **Present at z = 0** (first_material_rmse_gain_z_abs = 0.000000)
- Attributable to better global initialisation (OGTR_CF seed), not PT-aware coupling
- This is NOT a PT-sensitive gain; it does not demonstrate coupled-sector benefit

### 2. `pt_sensitive_gain` — Coupled-Sector Benefit
- Requires **small but nonzero z** (both abs_z_drift AND loss_eval_base improve)
- Onset interval (NOT a sharp threshold): **(0.016763, 0.021190]**
- ⚠️ The onset interval must NOT be over-interpreted as a sharp critical z value.
  Its width depends on the z_list resolution used in the sweep.

---

## Mask Sweep Validity

⚠️ **Pre-fix mask results are INVALID** and must NOT be used for scientific
conclusions. A v1 bug in `data_generator.py` caused PT scenarios to ignore
`mask_rate_override` (mask was always full-observed).

Only **post-fix runs** (after the `data_generator.py` fix) are valid.

**How to verify**: check `realized_mask_rate_mean` in
`table_phase1_mask_gain_summary.csv`. A valid sweep shows `realized_mask_rate_mean`
increasing with `requested_mask_rate`.

---

## Tables

| File | Contents |
|------|----------|
| `table_phase1_z_gain_summary.csv`    | z-axis two-layer gain (onset interval, material vs PT-sensitive) |
| `table_phase1_mask_gain_summary.csv` | mask-axis robustness (post-fix only, validity flag) |
| `table_phase1_snr_gain_summary.csv`  | SNR-axis robustness (strongest/weakest gain SNR) |
| `table_phase1_regime_summary.csv`    | Consolidated regime labels (4 rows) |

---

## Regime Labels

- `general_refinement_gain`: P0_OGTR_CF_INIT achieves general refinement gain (rmse_omega) over BL_OGTR_CF even at z=0 (classical-tangent regime). At...
- `pt_sensitive_onset`: PT-coupled sector benefit (abs_z_drift + loss_eval_base both improve) begins at small but nonzero z. Onset interval (NOT...
- `pt_sensitive_robust_snr_regime`: PT-sensitive gain is robust across tested SNR range. Loss improvement trend: attenuating....
- `pt_sensitive_robust_mask_regime`: PT-sensitive gain is robust across validated missing-rate range. Loss improvement trend: attenuating....
