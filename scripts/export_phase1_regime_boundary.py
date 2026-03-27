# SPDX-License-Identifier: GPL-3.0-or-later
"""
Phase I regime-boundary bundle exporter (exploratory).

Reads curated gain-oriented summary CSVs from pre-collected phase-axis inputs
and assembles a consolidated Phase I bundle under:
  artifacts/reporting/phase1_regime_boundary/<RUN_ID>/

This is an EXPLORATORY path, completely separate from the formal paper
pipeline (scripts/export_paper_summary.py).  Do NOT mix them.

Key design constraints reflected here:
- current-init-policy: theta_init from theta_init_from_true() + PARAMS offset
- mask sweep: only post-fix runs are valid (pre-fix ignored mask_rate_override)
- onset interval: must not be overinterpreted as a sharp critical threshold
- two-layer gain: material_rmse_gain (z=0) vs pt_sensitive_gain (nonzero z)
- Public-release note:
  This script is an optional export helper for curated reporting artifacts.
  It is not a full experiment execution pipeline.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_HEADLINE_METHOD = "P0_OGTR_CF_INIT"
_REF_METHOD      = "BL_OGTR_CF"

_Z_SUMMARY_FIELDS = [
    "headline_method",
    "reference_method",
    "first_material_rmse_gain_z_abs",
    "first_pt_sensitive_gain_z_abs",
    "last_no_pt_sensitive_gain_z_abs",
    "pt_sensitive_onset_interval",
    "note",
]

_MASK_SUMMARY_FIELDS = [
    "headline_method",
    "reference_method",
    "mask_sweep_validated",
    "requested_mask_rate_min",
    "requested_mask_rate_max",
    "realized_mask_rate_min",
    "realized_mask_rate_max",
    "observed_fraction_min",
    "observed_fraction_max",
    "all_pt_sensitive_gain",
    "all_material_rmse_gain",
    "loss_gain_trend",
    "note",
]

_SNR_SUMMARY_FIELDS = [
    "headline_method",
    "reference_method",
    "snr_min",
    "snr_max",
    "all_pt_sensitive_gain",
    "all_material_rmse_gain",
    "loss_gain_trend",
    "strongest_gain_snr",
    "weakest_gain_snr",
    "note",
]

_REGIME_FIELDS = [
    "regime_label",
    "condition",
    "headline_interpretation",
    "evidence_axis",
    "note",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(
    path: Path,
    rows: List[Dict[str, Any]],
    fieldnames: List[str],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _safe_float(val: object, default: float = float("nan")) -> float:
    try:
        return float(str(val))
    except (ValueError, TypeError):
        return default


def _parse_bool(val: object) -> Optional[bool]:
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    if s in ("true", "1", "yes"):
        return True
    if s in ("false", "0", "no", ""):
        return False
    return None


def _loss_trend(sorted_deltas: List[float]) -> str:
    """Conservatively classify a sorted list of delta_loss values.

    Negative delta = gain. Trend convention:
    - attenuating: all negative but gain shrinks toward 0 along the axis
    - flat: all negative and roughly constant, OR all non-negative (no gain)
    - mixed: inconsistent sign
    """
    fd = [d for d in sorted_deltas if math.isfinite(d)]
    if not fd:
        return "UNKNOWN"
    all_neg = all(d < 0 for d in fd)
    all_non_neg = all(d >= 0 for d in fd)
    if all_neg:
        if len(fd) >= 2 and fd[-1] > fd[0] + 1e-9:  # gain weakens along axis
            return "attenuating"
        return "flat"
    if all_non_neg:
        return "flat"
    return "mixed"

# ---------------------------------------------------------------------------
# Per-axis summary computers
# ---------------------------------------------------------------------------

def _compute_z_gain_summary(
    z_rows: List[Dict[str, str]],
    headline_method: str = _HEADLINE_METHOD,
    ref_method: str = _REF_METHOD,
) -> List[Dict[str, Any]]:
    """Distil z-axis into a single-row two-layer gain summary."""
    method_rows = [r for r in z_rows if r.get("method") == headline_method]
    if not method_rows:
        return [{
            "headline_method": headline_method,
            "reference_method": ref_method,
            "first_material_rmse_gain_z_abs": "NONE",
            "first_pt_sensitive_gain_z_abs":  "NONE",
            "last_no_pt_sensitive_gain_z_abs": "NONE",
            "pt_sensitive_onset_interval": "UNKNOWN",
            "note": "No rows found for headline_method in z_sweep_summary.",
        }]

    sorted_rows = sorted(
        method_rows, key=lambda r: _safe_float(r.get("z_abs", "nan"))
    )

    first_mat = next(
        (r for r in sorted_rows if _parse_bool(r.get("material_rmse_gain"))),
        None,
    )
    first_pt = next(
        (r for r in sorted_rows if _parse_bool(r.get("pt_sensitive_gain"))),
        None,
    )
    first_pt_z = _safe_float(first_pt["z_abs"]) if first_pt else float("nan")

    # Last z_abs BEFORE onset that is NOT pt_sensitive_gain
    if math.isfinite(first_pt_z):
        candidates = [
            r for r in sorted_rows
            if not _parse_bool(r.get("pt_sensitive_gain"))
            and _safe_float(r.get("z_abs")) < first_pt_z
        ]
        last_no_pt = max(
            candidates, key=lambda r: _safe_float(r.get("z_abs")), default=None
        )
    else:
        last_no_pt = None

    first_mat_z   = _safe_float(first_mat["z_abs"])   if first_mat   else float("nan")
    last_no_pt_z  = _safe_float(last_no_pt["z_abs"])  if last_no_pt  else float("nan")

    if math.isfinite(last_no_pt_z) and math.isfinite(first_pt_z):
        onset_interval = f"({last_no_pt_z:.6f}, {first_pt_z:.6f}]"
    elif math.isfinite(first_pt_z):
        onset_interval = f"(UNKNOWN, {first_pt_z:.6f}]"
    else:
        onset_interval = "UNKNOWN"

    note = "; ".join([
        (f"material_rmse_gain first z_abs={first_mat_z:.6f}"
         if math.isfinite(first_mat_z) else "material_rmse_gain not observed"),
        f"pt_sensitive_gain onset interval: {onset_interval}",
        "onset interval is NOT a sharp critical threshold — "
        "interval width depends on z_list resolution",
    ])

    return [{
        "headline_method": headline_method,
        "reference_method": ref_method,
        "first_material_rmse_gain_z_abs":
            f"{first_mat_z:.6f}" if math.isfinite(first_mat_z)  else "NONE",
        "first_pt_sensitive_gain_z_abs":
            f"{first_pt_z:.6f}" if math.isfinite(first_pt_z)   else "NONE",
        "last_no_pt_sensitive_gain_z_abs":
            f"{last_no_pt_z:.6f}" if math.isfinite(last_no_pt_z) else "NONE",
        "pt_sensitive_onset_interval": onset_interval,
        "note": note,
    }]


def _compute_mask_gain_summary(
    mask_rows: List[Dict[str, str]],
    headline_method: str = _HEADLINE_METHOD,
    ref_method: str = _REF_METHOD,
) -> List[Dict[str, Any]]:
    """Distil mask-axis (post-fix only) into a single-row validity-aware summary."""
    method_rows = [r for r in mask_rows if r.get("method") == headline_method]

    _invalid_note = (
        "IMPORTANT: pre-fix mask results are INVALID (PT scenarios ignored "
        "mask_rate_override). Only post-fix runs are valid for scientific conclusions."
    )

    if not method_rows:
        return [{
            "headline_method": headline_method,
            "reference_method": ref_method,
            "mask_sweep_validated": False,
            "requested_mask_rate_min": "NONE",
            "requested_mask_rate_max": "NONE",
            "realized_mask_rate_min":  "NONE",
            "realized_mask_rate_max":  "NONE",
            "observed_fraction_min":   "NONE",
            "observed_fraction_max":   "NONE",
            "all_pt_sensitive_gain":   False,
            "all_material_rmse_gain":  False,
            "loss_gain_trend":         "NONE",
            "note": f"No rows found for headline_method. {_invalid_note}",
        }]

    sorted_rows = sorted(
        method_rows,
        key=lambda r: _safe_float(r.get("requested_mask_rate", "nan")),
    )

    req_mrs   = [_safe_float(r.get("requested_mask_rate"))   for r in sorted_rows]
    real_mrs  = [_safe_float(r.get("realized_mask_rate_mean")) for r in sorted_rows]
    obs_fracs = [_safe_float(r.get("observed_fraction_mean")) for r in sorted_rows]

    vr = [v for v in real_mrs  if math.isfinite(v)]
    vo = [v for v in obs_fracs if math.isfinite(v)]

    # Validity: realized increases & observed_fraction decreases
    mask_validated = False
    if len(vr) >= 2 and len(vo) >= 2:
        inc = sum(1 for a, b in zip(vr, vr[1:]) if b > a)
        dec = sum(1 for a, b in zip(vo, vo[1:]) if b < a)
        mask_validated = inc >= max(1, len(vr) // 2) and dec >= max(1, len(vo) // 2)

    all_pt  = all(_parse_bool(r.get("pt_sensitive_gain"))  for r in sorted_rows)
    all_mat = all(_parse_bool(r.get("material_rmse_gain")) for r in sorted_rows)

    deltas = [_safe_float(r.get("delta_loss_eval_base_vs_bl_ogtr_cf")) for r in sorted_rows]
    trend  = _loss_trend(deltas)

    vq  = [v for v in req_mrs if math.isfinite(v)]

    return [{
        "headline_method": headline_method,
        "reference_method": ref_method,
        "mask_sweep_validated": mask_validated,
        "requested_mask_rate_min": f"{min(vq):.3f}"  if vq else "NONE",
        "requested_mask_rate_max": f"{max(vq):.3f}"  if vq else "NONE",
        "realized_mask_rate_min":  f"{min(vr):.3f}"  if vr else "NONE",
        "realized_mask_rate_max":  f"{max(vr):.3f}"  if vr else "NONE",
        "observed_fraction_min":   f"{min(vo):.3f}"  if vo else "NONE",
        "observed_fraction_max":   f"{max(vo):.3f}"  if vo else "NONE",
        "all_pt_sensitive_gain":   all_pt,
        "all_material_rmse_gain":  all_mat,
        "loss_gain_trend":         trend,
        "note": (
            f"Sweep validation: {'PASS' if mask_validated else 'FAIL — check realized_mask_rate_mean'}. "
            + _invalid_note
        ),
    }]


def _compute_snr_gain_summary(
    snr_rows: List[Dict[str, str]],
    headline_method: str = _HEADLINE_METHOD,
    ref_method: str = _REF_METHOD,
) -> List[Dict[str, Any]]:
    """Distil SNR-axis into a single-row gain-robustness summary."""
    method_rows = [r for r in snr_rows if r.get("method") == headline_method]

    if not method_rows:
        return [{
            "headline_method": headline_method,
            "reference_method": ref_method,
            "snr_min": "NONE", "snr_max": "NONE",
            "all_pt_sensitive_gain": False, "all_material_rmse_gain": False,
            "loss_gain_trend": "NONE",
            "strongest_gain_snr": "NONE", "weakest_gain_snr": "NONE",
            "note": "No rows found for headline_method in snr sweep summary.",
        }]

    sorted_rows = sorted(
        method_rows, key=lambda r: _safe_float(r.get("snr_db", "nan"))
    )
    snr_vals = [_safe_float(r.get("snr_db")) for r in sorted_rows]
    vs = [v for v in snr_vals if math.isfinite(v)]

    all_pt  = all(_parse_bool(r.get("pt_sensitive_gain"))  for r in sorted_rows)
    all_mat = all(_parse_bool(r.get("material_rmse_gain")) for r in sorted_rows)

    deltas = [_safe_float(r.get("delta_loss_eval_base_vs_bl_ogtr_cf")) for r in sorted_rows]
    trend  = _loss_trend(deltas)

    # Strongest/weakest gain = most/least negative delta_loss
    paired = [
        (snr_vals[i], deltas[i])
        for i in range(len(sorted_rows))
        if math.isfinite(snr_vals[i]) and math.isfinite(deltas[i])
    ]
    if paired:
        strongest_snr = f"{min(paired, key=lambda p: p[1])[0]:.1f}"
        weakest_snr   = f"{max(paired, key=lambda p: p[1])[0]:.1f}"
    else:
        strongest_snr = weakest_snr = "NONE"

    return [{
        "headline_method": headline_method,
        "reference_method": ref_method,
        "snr_min": f"{min(vs):.1f}" if vs else "NONE",
        "snr_max": f"{max(vs):.1f}" if vs else "NONE",
        "all_pt_sensitive_gain":  all_pt,
        "all_material_rmse_gain": all_mat,
        "loss_gain_trend":        trend,
        "strongest_gain_snr":     strongest_snr,
        "weakest_gain_snr":       weakest_snr,
        "note": (
            "strongest/weakest_gain_snr based on delta_loss_eval_base_vs_bl_ogtr_cf "
            "(most negative = strongest PT-base-loss improvement). "
            "Phase I current-init-policy applies. "
            "Low-k smoke runs must NOT be used for scientific robustness conclusions."
        ),
    }]


def _compute_regime_summary(
    z_table:    List[Dict[str, Any]],
    mask_table: List[Dict[str, Any]],
    snr_table:  List[Dict[str, Any]],
    headline_method: str = _HEADLINE_METHOD,
    ref_method:      str = _REF_METHOD,
) -> List[Dict[str, Any]]:
    """Produce consolidated 4-row regime label table."""
    z_row    = z_table[0]    if z_table    else {}
    mask_row = mask_table[0] if mask_table else {}
    snr_row  = snr_table[0]  if snr_table  else {}

    first_mat_z    = z_row.get("first_material_rmse_gain_z_abs", "NONE")
    onset_interval = z_row.get("pt_sensitive_onset_interval", "UNKNOWN")

    mask_validated = mask_row.get("mask_sweep_validated", False)
    mask_all_pt    = mask_row.get("all_pt_sensitive_gain", False)
    mask_trend     = mask_row.get("loss_gain_trend", "UNKNOWN")

    snr_all_pt  = snr_row.get("all_pt_sensitive_gain", False)
    snr_trend   = snr_row.get("loss_gain_trend", "UNKNOWN")

    return [
        {
            "regime_label": "general_refinement_gain",
            "condition": (
                f"z=0, material_rmse_gain=True but pt_sensitive_gain=False "
                f"(headline={headline_method})"
            ),
            "headline_interpretation": (
                f"{headline_method} achieves general refinement gain (rmse_omega) "
                f"over {ref_method} even at z=0 (classical-tangent regime). "
                "Attributable to better global initialisation (OGTR_CF seed), "
                "not PT-sensitive refinement."
            ),
            "evidence_axis": "z_sweep (z_abs=0.0)",
            "note": (
                f"first_material_rmse_gain_z_abs={first_mat_z}. "
                "Does NOT require nonzero z."
            ),
        },
        {
            "regime_label": "pt_sensitive_onset",
            "condition": "low-z sweep: first z_abs where pt_sensitive_gain becomes True",
            "headline_interpretation": (
                "PT-coupled sector benefit (abs_z_drift + loss_eval_base both improve) "
                f"begins at small but nonzero z. "
                f"Onset interval (NOT a sharp threshold): {onset_interval}"
            ),
            "evidence_axis": "z_sweep (low-z refinement)",
            "note": (
                f"Onset interval: {onset_interval}. "
                "Interval width depends on z_list resolution; denser grid → narrower interval. "
                "DO NOT interpret as a sharp critical z value."
            ),
        },
        {
            "regime_label": "pt_sensitive_robust_snr_regime",
            "condition": (
                f"SNR sweep: all_pt_sensitive_gain={snr_all_pt}, "
                f"loss_gain_trend={snr_trend}"
            ),
            "headline_interpretation": (
                ("PT-sensitive gain is robust across tested SNR range. "
                 if snr_all_pt else
                 "PT-sensitive gain is NOT uniformly robust across tested SNR points. ")
                + f"Loss improvement trend: {snr_trend}."
            ),
            "evidence_axis": "pt_snr_sweep (S_PT_zNZ_strong)",
            "note": (
                "Phase I current-init-policy. "
                "Low-k smoke runs must NOT be used as scientific robustness evidence."
            ),
        },
        {
            "regime_label": "pt_sensitive_robust_mask_regime",
            "condition": (
                f"mask sweep (post-fix only): validated={mask_validated}, "
                f"all_pt_sensitive_gain={mask_all_pt}, "
                f"loss_gain_trend={mask_trend}"
            ),
            "headline_interpretation": (
                ("PT-sensitive gain is robust across validated missing-rate range. "
                 if (mask_all_pt and mask_validated) else
                 "PT-sensitive gain is NOT uniformly robust, or sweep validation failed. ")
                + f"Loss improvement trend: {mask_trend}."
            ),
            "evidence_axis": "pt_mask_sweep (post-fix only)",
            "note": (
                "Pre-fix mask results are INVALID (PT scenarios silently ignored "
                "mask_rate_override before the data_generator.py fix). "
                "Only post-fix runs contribute to this conclusion. "
                f"Sweep validation: {'PASS' if mask_validated else 'FAIL'}."
            ),
        },
    ]


# ---------------------------------------------------------------------------
# README builder
# ---------------------------------------------------------------------------

def _make_readme(
    run_id:          str,
    headline_method: str,
    ref_method:      str,
    z_table:         List[Dict[str, Any]],
    regime_table:    List[Dict[str, Any]],
) -> str:
    z_row = z_table[0] if z_table else {}
    onset = z_row.get("pt_sensitive_onset_interval", "UNKNOWN")
    first_mat = z_row.get("first_material_rmse_gain_z_abs", "NONE")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return f"""\
# Phase I Regime-Boundary Bundle

**RUN_ID**: {run_id}  
**Generated (UTC)**: {timestamp}

---

## ⚠️ Status

This is an **EXPLORATORY Phase I bundle**, NOT a formal paper artifact.  
It is produced by `scripts/export_phase1_regime_boundary.py` and must be
interpreted under the following constraints:

- **Current-init-policy**: θ_init is derived from `theta_init_from_true()` +
  PARAMS.json offset. The `z_override` changes `theta_true.z` only;
  estimator initialisation is NOT altered.
- **Headline method**: `{headline_method}`
- **Reference method**: `{ref_method}`
- **Scope**: Phase I boundary analysis only. For formal paper experiments,
  see `artifacts/reporting/paper_runs/` produced by the separate
  `paper_experiments` pipeline.

---

## Core Phase I Findings: Two-Layer Gain Structure

### 1. `material_rmse_gain` — General Refinement Gain
- **Present at z = 0** (first_material_rmse_gain_z_abs = {first_mat})
- Attributable to better global initialisation (OGTR_CF seed), not PT-aware coupling
- This is NOT a PT-sensitive gain; it does not demonstrate coupled-sector benefit

### 2. `pt_sensitive_gain` — Coupled-Sector Benefit
- Requires **small but nonzero z** (both abs_z_drift AND loss_eval_base improve)
- Onset interval (NOT a sharp threshold): **{onset}**
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

{chr(10).join(f'- `{r["regime_label"]}`: {r["headline_interpretation"][:120]}...' for r in regime_table)}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Export Phase I regime-boundary bundle (exploratory)."
    )
    p.add_argument(
        "--input_base",
        default="./phase1_regime_boundary_out",
        help="Directory containing z_sweep/, pt_mask_sweep/, pt_snr_sweep/ subdirs.",
    )
    p.add_argument(
        "--output_base",
        default="artifacts/reporting/phase1_regime_boundary",
        help="Parent directory for output bundles.",
    )
    p.add_argument(
        "--headline_method", default=_HEADLINE_METHOD,
        help="Primary method to analyse (default: P0_OGTR_CF_INIT).",
    )
    p.add_argument(
        "--ref_method", default=_REF_METHOD,
        help="Reference baseline (default: BL_OGTR_CF).",
    )
    p.add_argument(
        "--dry_run", action="store_true",
        help="Print what would be written without creating files.",
    )
    args = p.parse_args(argv)

    input_base = Path(args.input_base)

    z_csv    = input_base / "z_sweep"      / "artifacts" / "z_sweep_summary.csv"
    mask_csv = input_base / "pt_mask_sweep" / "artifacts" / "pt_mask_sweep_summary.csv"
    snr_csv  = input_base / "pt_snr_sweep"  / "artifacts" / "pt_snr_sweep_summary.csv"

    z_rows    = _read_csv(z_csv)
    mask_rows = _read_csv(mask_csv)
    snr_rows  = _read_csv(snr_csv)

    if not z_rows:
        print(f"[warn] z_sweep summary not found or empty: {z_csv}")
    if not mask_rows:
        print(f"[warn] pt_mask_sweep summary not found or empty: {mask_csv}")
    if not snr_rows:
        print(f"[warn] pt_snr_sweep summary not found or empty: {snr_csv}")

    z_table      = _compute_z_gain_summary(z_rows,    args.headline_method, args.ref_method)
    mask_table   = _compute_mask_gain_summary(mask_rows, args.headline_method, args.ref_method)
    snr_table    = _compute_snr_gain_summary(snr_rows,  args.headline_method, args.ref_method)
    regime_table = _compute_regime_summary(
        z_table, mask_table, snr_table,
        args.headline_method, args.ref_method,
    )

    run_id   = datetime.now(timezone.utc).strftime("phase1_%Y%m%dT%H%M%SZ")
    out_root = Path(args.output_base) / run_id

    if args.dry_run:
        print(f"[dry-run] would write Phase I bundle to: {out_root}")
        print(f"  tables: {_Z_SUMMARY_FIELDS[:2]!r}  …")
        return 0

    out_root.mkdir(parents=True, exist_ok=True)

    _write_csv(out_root / "table_phase1_z_gain_summary.csv",    z_table,      _Z_SUMMARY_FIELDS)
    _write_csv(out_root / "table_phase1_mask_gain_summary.csv", mask_table,   _MASK_SUMMARY_FIELDS)
    _write_csv(out_root / "table_phase1_snr_gain_summary.csv",  snr_table,    _SNR_SUMMARY_FIELDS)
    _write_csv(out_root / "table_phase1_regime_summary.csv",    regime_table, _REGIME_FIELDS)

    manifest = {
        "run_id":            run_id,
        "generated_utc":     datetime.now(timezone.utc).isoformat(),
        "bundle_type":       "exploratory_phase1_regime_boundary",
        "headline_method":   args.headline_method,
        "reference_method":  args.ref_method,
        "current_init_policy": True,
        "mask_sweep_validity": (
            "post-fix only — pre-fix runs are invalid "
            "(PT scenarios ignored mask_rate_override before data_generator.py fix)"
        ),
        "onset_interval_note": (
            "onset interval is NOT a sharp critical threshold; "
            "width depends on z_list resolution"
        ),
        "tables": [
            "table_phase1_z_gain_summary.csv",
            "table_phase1_mask_gain_summary.csv",
            "table_phase1_snr_gain_summary.csv",
            "table_phase1_regime_summary.csv",
        ],
        "input_sources": {
            "z_sweep":       str(z_csv),
            "pt_mask_sweep": str(mask_csv),
            "pt_snr_sweep":  str(snr_csv),
        },
    }
    (out_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    readme = _make_readme(run_id, args.headline_method, args.ref_method,
                          z_table, regime_table)
    (out_root / "README.md").write_text(readme, encoding="utf-8")

    # Update latest.txt in output_base (not in out_root)
    latest = Path(args.output_base) / "latest.txt"
    latest.write_text(run_id + "\n", encoding="utf-8")

    print(f"[done] Phase I regime-boundary bundle written to: {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
