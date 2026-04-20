#!/usr/bin/env python3
"""Export paper-facing summary from latest collected TSP pack runs.

Reads artifacts/packs/<pack>/latest.txt for each TSP pack, then assembles
a unified, read-only view under:

    artifacts/reporting/paper_runs/<PAPER_RUN_ID>/

Output layout:
    summary_baseline.csv   - top-level aggregate from baseline_pack run
    summary_stress.csv     - top-level aggregate from stress_sweep run
    summary_n_sweep.csv    - top-level aggregate from n_sweep run
    summary_coupling.csv   - top-level aggregate from coupling_pack run
    figures/<pack>/        - key figures copied from each pack run
    manifest.json          - provenance (pack run_ids, git sha, timestamp)
    README.md              - navigation guide

Usage:
    python scripts/export_paper_summary.py
    python scripts/export_paper_summary.py --outdir artifacts/reporting/paper_runs
    python scripts/export_paper_summary.py --dry-run

The output directory is written to artifacts/reporting/paper_runs/latest.txt
so downstream scripts can find the most recent paper run.

Public-release note:
    This script is an optional export helper for assembling curated paper-facing
    bundles from already-collected artifacts. It is not a full benchmark
    execution pipeline.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_ROOT = REPO_ROOT / "artifacts"

# (pack_name, source_csv_in_run_artifacts, summary_csv, table_alias_csv)
# Both summary_* and table_* are written; table_* is the paper-facing alias.
PACK_SUMMARIES: List[Tuple[str, str, str, str]] = [
    ("baseline_pack", "baseline_summary.csv", "summary_baseline.csv", "table_main_baseline.csv"),
    ("stress_sweep",  "stress_summary.csv",   "summary_stress.csv",   "table_stress_missing.csv"),
    ("n_sweep",       "n_sweep_summary.csv",  "summary_n_sweep.csv",  "table_n_scaling.csv"),
    ("coupling_pack", "coupling_summary.csv", "summary_coupling.csv", "table_coupling.csv"),
]

# Glob patterns for figures to copy per pack (relative to run_root/figures/)
PACK_FIGURE_GLOBS: Dict[str, List[str]] = {
    "baseline_pack": [
        "baseline_rmse_vs_eval_*.png",
        "baseline_rmse_vs_runtime_*.png",
        "baseline_cactus_*.png",
    ],
    "stress_sweep": [
        "stress_missing_vs_rmse_omega.png",
    ],
    "n_sweep": [
        "n_vs_runtime_*.png",
        "n_vs_evals_*.png",
        "n_vs_rmse_omega_*.png",
    ],
    "coupling_pack": [
        "coupling_vs_rmse_omega.png",
        "coupling_vs_missing_rate.png",
    ],
}

# Figure role classification rules: (glob_pattern, role)
# role is "main" (suitable for main manuscript) or "appendix" (supplementary/appendix).
FIGURE_ROLE_RULES: List[Tuple[str, str]] = [
    ("baseline_rmse_vs_eval_*.png",      "main"),
    ("stress_missing_vs_rmse_omega.png", "main"),
    ("n_vs_rmse_omega_*.png",            "main"),
    ("baseline_rmse_vs_runtime_*.png",   "appendix"),
    ("baseline_cactus_*.png",            "appendix"),
    ("n_vs_runtime_*.png",               "appendix"),
    ("n_vs_evals_*.png",                 "appendix"),
    ("coupling_vs_rmse_omega.png",       "appendix"),
    ("coupling_vs_missing_rate.png",     "appendix"),
]


def _git_sha8() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()[:8]
    except Exception:
        return "nogit"


def _utc_now_compact() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def _find_latest_run(pack_name: str, artifacts_root: Path) -> Optional[Path]:
    """Return the latest run directory for a pack, or None if not found."""
    pack_dir = artifacts_root / "packs" / pack_name
    latest_txt = pack_dir / "latest.txt"
    if not latest_txt.is_file():
        return None
    run_id = latest_txt.read_text(encoding="utf-8").strip()
    run_dir = pack_dir / run_id
    return run_dir if run_dir.is_dir() else None


def _classify_figure(fname: str) -> str:
    """Return 'main', 'appendix', or 'unclassified' for a figure filename."""
    for pattern, role in FIGURE_ROLE_RULES:
        if fnmatch(fname, pattern):
            return role
    return "unclassified"


def _classify_all_figures(figures_root: Path) -> dict:
    """Scan figures_root recursively and classify each .png by FIGURE_ROLE_RULES.

    Returns a dict with keys:
      figure_roles: {rel_path: role}
      recommended_main_figures: [rel_path, ...]
      recommended_appendix_figures: [rel_path, ...]
    """
    figure_roles: Dict[str, str] = {}
    main_figs: List[str] = []
    appendix_figs: List[str] = []

    if not figures_root.is_dir():
        return {
            "figure_roles": figure_roles,
            "recommended_main_figures": main_figs,
            "recommended_appendix_figures": appendix_figs,
        }

    for fig in sorted(figures_root.rglob("*.png")):
        rel = fig.relative_to(figures_root).as_posix()
        role = _classify_figure(fig.name)
        figure_roles[rel] = role
        if role == "main":
            main_figs.append(rel)
        elif role == "appendix":
            appendix_figs.append(rel)

    return {
        "figure_roles": figure_roles,
        "recommended_main_figures": main_figs,
        "recommended_appendix_figures": appendix_figs,
    }


def _copy_pack_figures(
    pack_name: str,
    run_dir: Path,
    dst_figures_root: Path,
    dry_run: bool,
) -> List[str]:
    """Copy key figures from a pack run into dst_figures_root/<pack_name>/."""
    src_figures = run_dir / "figures"
    if not src_figures.is_dir():
        return []

    globs = PACK_FIGURE_GLOBS.get(pack_name, [])
    pack_dst = dst_figures_root / pack_name
    copied: List[str] = []

    for pattern in globs:
        for src_fig in sorted(src_figures.glob(pattern)):
            if dry_run:
                print(f"    [dry-run] figure: {pack_name}/{src_fig.name}")
            else:
                pack_dst.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_fig, pack_dst / src_fig.name)
            copied.append(src_fig.name)

    return copied


def _write_readme(out_dir: Path, manifest: dict) -> None:
    lines = [
        "# Paper Run Summary",
        "",
        f"Generated:     {manifest['generated_at']}",
        f"PAPER_RUN_ID:  `{manifest['paper_run_id']}`",
        f"Git SHA-8:     `{manifest['git_sha8']}`",
        "",
        "## Summary / table files",
        "",
        "Each pack produces two files (same content, two naming conventions):",
        "",
    ]
    for pack_name, _src, summary_csv, table_csv in PACK_SUMMARIES:
        info = manifest["sources"].get(pack_name, {})
        run_id = info.get("run_id", "(missing)")
        lines.append(f"- `{summary_csv}` / `{table_csv}` — {pack_name}  (run_id: `{run_id}`)")
    lines += [
        "",
        "## Figures",
        "",
        "Key figures are copied into `figures/<pack_name>/`.",
        "Main-manuscript figures: see `manifest.json` → `recommended_main_figures`.",
        "Appendix/supplementary: see `manifest.json` → `recommended_appendix_figures`.",
        "",
        "## Traceability",
        "",
        "- This directory is the read-only public assembled paper-run reporting snapshot.",
        "- Source pack run IDs are listed above and in `manifest.json`; raw pack roots are provenance-only origins and are not included as local `artifacts/packs/<pack>/<RUN_ID>/` directories in this public repository.",
        "- Reassembly and experiment regeneration belong to the execution workspace, not this public technical anchor.",
        "",
    ]
    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Export paper-facing summary from collected TSP pack runs."
    )
    ap.add_argument(
        "--outdir",
        default=str(ARTIFACTS_ROOT / "reporting" / "paper_runs"),
        help=(
            "Parent directory; output goes to <outdir>/<PAPER_RUN_ID>/. "
            "Default: artifacts/reporting/paper_runs"
        ),
    )
    ap.add_argument(
        "--artifacts-root",
        default=str(ARTIFACTS_ROOT),
        help=(
            "Root of the artifacts tree to read from. "
            "Default: artifacts/ relative to repo root. "
            "Override in tests to use a temporary directory."
        ),
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without writing anything.",
    )
    args = ap.parse_args()

    artifacts_root = Path(args.artifacts_root)

    paper_run_id = f"paper_run__{_utc_now_compact()}__{_git_sha8()}"
    out_root = Path(args.outdir) / paper_run_id

    rel_out = out_root.relative_to(REPO_ROOT) if out_root.is_relative_to(REPO_ROOT) else out_root
    print(f"[export] PAPER_RUN_ID : {paper_run_id}")
    print(f"[export] output       : {rel_out}")

    # Build summary-to-table mapping up front for the manifest
    summary_to_table_map: Dict[str, str] = {
        summary_csv: table_csv
        for _, _, summary_csv, table_csv in PACK_SUMMARIES
    }

    manifest: dict = {
        "schema_version": 2,
        "paper_run_id": paper_run_id,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "git_sha8": _git_sha8(),
        "sources": {},
        "summary_files": {},
        "table_aliases": {},
        "summary_to_table_map": summary_to_table_map,
        "figure_counts": {},
        "missing_packs": [],
    }

    if not args.dry_run:
        out_root.mkdir(parents=True, exist_ok=True)
        (out_root / "figures").mkdir(exist_ok=True)

    # --- Copy summary CSVs (dual output: summary_* AND table_*) ---
    for pack_name, src_csv_name, summary_csv_name, table_csv_name in PACK_SUMMARIES:
        run_dir = _find_latest_run(pack_name, artifacts_root)

        if run_dir is None:
            print(f"  [warn] {pack_name}: no collected run found in artifacts/packs/. Skipping.")
            manifest["missing_packs"].append(pack_name)
            continue

        src_csv = run_dir / "artifacts" / src_csv_name
        if not src_csv.is_file():
            print(f"  [warn] {pack_name}: {src_csv_name} not found in run artifacts. Skipping.")
            manifest["missing_packs"].append(pack_name)
            continue

        run_id = run_dir.name
        manifest["sources"][pack_name] = {
            "run_id": run_id,
            "run_dir": str(
                run_dir.relative_to(REPO_ROOT) if run_dir.is_relative_to(REPO_ROOT) else run_dir
            ),
            "src_csv": src_csv_name,
        }
        manifest["summary_files"][pack_name] = summary_csv_name
        manifest["table_aliases"][pack_name] = table_csv_name

        if args.dry_run:
            print(f"  [dry-run] {pack_name}: would copy {src_csv_name}")
            print(f"            -> {summary_csv_name} + {table_csv_name}")
        else:
            # Write both the summary_* alias and the table_* alias (same content)
            shutil.copy2(src_csv, out_root / summary_csv_name)
            shutil.copy2(src_csv, out_root / table_csv_name)
            print(f"  [ok] {pack_name}: {summary_csv_name} + {table_csv_name}")

        # Copy figures
        copied_figs = _copy_pack_figures(
            pack_name, run_dir, out_root / "figures", dry_run=args.dry_run
        )
        manifest["figure_counts"][pack_name] = len(copied_figs)
        if copied_figs and not args.dry_run:
            print(f"       figures: {len(copied_figs)} copied to figures/{pack_name}/")

    if args.dry_run:
        print(f"\n[dry-run] done. Would create: {paper_run_id}")
        return 0

    # --- Classify all copied figures into main / appendix ---
    figure_classification = _classify_all_figures(out_root / "figures")
    manifest.update(figure_classification)

    # --- Write manifest and README ---
    (out_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    _write_readme(out_root, manifest)

    # --- Update latest.txt pointer ---
    latest_path = Path(args.outdir) / "latest.txt"
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.write_text(paper_run_id + "\n", encoding="utf-8")

    if manifest["missing_packs"]:
        print(
            f"\n[warn] {len(manifest['missing_packs'])} pack(s) had no collected run: "
            f"{manifest['missing_packs']}"
        )
        print("       Reassemble required source packs in the execution workspace first.")
        return 1

    rel_out_done = out_root.relative_to(REPO_ROOT) if out_root.is_relative_to(REPO_ROOT) else out_root
    print(f"\n[done] {rel_out_done}/")
    print(f"       latest pointer: {latest_path.relative_to(REPO_ROOT) if latest_path.is_relative_to(REPO_ROOT) else latest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
