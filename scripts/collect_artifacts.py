#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect evidence artifacts into a canonical repo-level artifacts/ tree.

Usage:
  python scripts/collect_artifacts.py --all
  python scripts/collect_artifacts.py --pack qfrt_vs_fft_pack
  python scripts/collect_artifacts.py --all --mode symlink   # if you prefer symlinks
  python scripts/collect_artifacts.py --all --dry-run

Notes:
- Default is copy mode for submission-friendly "Evidence Pack".
- Packs choose the newest (by mtime) candidate directory, ignoring "*smoke*" unless no other choice.
- Public-release note:
  This script is an optional collection/export helper. It is not the full
  execution pipeline and may expect runtime-generated source directories that
  are outside a minimal public evidence snapshot.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class GitState:
    commit: str
    branch: str
    dirty: bool

    @staticmethod
    def detect() -> "GitState":
        def run(cmd: List[str]) -> str:
            try:
                out = subprocess.check_output(cmd, cwd=REPO_ROOT, stderr=subprocess.DEVNULL)
                return out.decode("utf-8", errors="replace").strip()
            except Exception:
                return ""

        commit = run(["git", "rev-parse", "HEAD"])
        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        status = run(["git", "status", "--porcelain"])
        dirty = bool(status)
        return GitState(commit=commit, branch=branch, dirty=dirty)

    def sha8(self) -> str:
        return (self.commit or "nogit")[:8]


@dataclass
class PackSpec:
    name: str
    candidates: List[str]  # relative to repo root
    prefer_non_smoke: bool = True


DEFAULT_PACKS: List[PackSpec] = [
    PackSpec(
        name="qfrt_vs_fft_pack",
        candidates=["qfrt_vs_fft_pack_run", "_verify_qfrt_vs_fft_pack_out"],
    ),
    PackSpec(
        name="init_sweep_pack",
        candidates=["init_sweep_pack_out", "init_sweep_smoke_out"],
    ),
    PackSpec(
        name="omega_fix_pack",
        candidates=["omega_fix_pack_out", "omega_fix_pack_smoke_out"],
    ),
    PackSpec(
        name="run_aggr_safe",
        candidates=["run_aggr_safe_v2", "run_aggr_safe"],
    ),
    PackSpec(
        name="run_aggr_strict",
        candidates=["run_aggr_strict_v2", "run_aggr_strict"],
    ),
    # TSP-oriented diagnostic packs (Batch 1-4)
    PackSpec(
        name="baseline_pack",
        candidates=["baseline_pack_full_out", "baseline_pack_smoke_out"],
    ),
    PackSpec(
        name="stress_sweep",
        candidates=["stress_sweep_full_out", "stress_sweep_smoke_out"],
    ),
    PackSpec(
        name="n_sweep",
        candidates=["n_sweep_full_out", "n_sweep_smoke_out"],
    ),
    PackSpec(
        name="coupling_pack",
        candidates=["coupling_pack_full_out", "coupling_pack_smoke_out"],
    ),
]


def utc_now_compact(local_tz: bool = True) -> str:
    # Use local time for human sort; paper evidence packs usually want local timestamp
    now = dt.datetime.now() if local_tz else dt.datetime.utcnow()
    return now.strftime("%Y%m%d-%H%M%S")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def is_smoke_path(p: Path) -> bool:
    s = str(p).lower()
    return "smoke" in s


def pick_best_candidate(spec: PackSpec) -> Optional[Path]:
    existing = [REPO_ROOT / c for c in spec.candidates if (REPO_ROOT / c).is_dir()]
    if not existing:
        return None

    # Prefer non-smoke if possible
    if spec.prefer_non_smoke:
        non_smoke = [p for p in existing if not is_smoke_path(p)]
        if non_smoke:
            existing = non_smoke

    # Pick newest by mtime
    existing.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return existing[0]


def derive_tag(spec: PackSpec, src_dir: Path) -> str:
    name = src_dir.name.lower()
    if "smoke" in name:
        return "smoke"
    if name.endswith("_v2"):
        return "v2"
    if spec.name.startswith("run_aggr_") and "definition" in name:
        return "definition-locked"
    return "main"


def find_config_snapshot(src_dir: Path) -> Optional[Path]:
    # Priority 1: pack-out artifacts config snapshot
    p1 = src_dir / "artifacts" / "config_snapshot.json"
    if p1.is_file():
        return p1

    # Priority 2: reporting generated snapshot
    p2 = REPO_ROOT / "docs" / "_generated" / "artifacts" / "reporting" / "config_snapshot.json"
    if p2.is_file():
        return p2

    # Priority 3: appendix figures snapshot
    p3 = REPO_ROOT / "figures" / "artifacts" / "appendix" / "config_snapshot.json"
    if p3.is_file():
        return p3

    return None


def cfg_hash8(cfg_path: Optional[Path]) -> Tuple[str, Optional[str]]:
    if cfg_path and cfg_path.is_file():
        h = sha256_file(cfg_path)
        return h[:8], h
    # fall back: stable placeholder
    h = sha256_bytes(b"nocfg")
    return h[:8], h


def copy_tree(src: Path, dst: Path, mode: str) -> None:
    if not src.exists():
        return
    safe_mkdir(dst)

    for root, dirs, files in os.walk(src):
        root_p = Path(root)
        rel = root_p.relative_to(src)
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for d in dirs:
            (dst / rel / d).mkdir(parents=True, exist_ok=True)
        for fn in files:
            s = root_p / fn
            t = dst / rel / fn

            if t.exists():
                # keep deterministic; overwrite
                if t.is_symlink() or t.is_file():
                    t.unlink()
                else:
                    shutil.rmtree(t)

            if mode == "copy":
                shutil.copy2(s, t)
            elif mode == "symlink":
                # relative symlink if possible
                try:
                    rel_target = os.path.relpath(s, start=t.parent)
                    t.symlink_to(rel_target)
                except Exception:
                    t.symlink_to(s)
            elif mode == "hardlink":
                os.link(s, t)
            else:
                raise ValueError(f"Unknown mode: {mode}")


def write_json(path: Path, obj: dict) -> None:
    safe_mkdir(path.parent)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_run_index(index_csv: Path, index_jsonl: Path, row: dict) -> None:
    safe_mkdir(index_csv.parent)

    # CSV (create header if missing)
    csv_exists = index_csv.exists()
    fieldnames = ["created_at", "pack", "run_id", "tag", "git_sha8", "cfg8", "src_dir"]
    with index_csv.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not csv_exists:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in fieldnames})

    # JSONL
    with index_jsonl.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def compute_checksums(root: Path, out_path: Path, exclude_names: Optional[set] = None) -> None:
    exclude_names = exclude_names or set()
    lines: List[str] = []

    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        if p.name in exclude_names:
            continue
        # avoid self-including checksum file
        if p.resolve() == out_path.resolve():
            continue

        rel = p.relative_to(root)
        h = sha256_file(p)
        lines.append(f"{h}  {rel.as_posix()}")

    safe_mkdir(out_path.parent)
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def snapshot_env(artifacts_root: Path) -> None:
    env_dir = artifacts_root / "env"
    safe_mkdir(env_dir)

    (env_dir / "python_version.txt").write_text(
        sys.version.replace("\n", " ") + "\n", encoding="utf-8"
    )
    (env_dir / "platform.txt").write_text(
        f"{platform.platform()}\n", encoding="utf-8"
    )

    # requirements lock (best-effort)
    req = ""
    try:
        req = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", errors="replace")
    except Exception:
        req = "# pip freeze failed (pip not available?)\n"
    (env_dir / "requirements.lock.txt").write_text(req if req.endswith("\n") else req + "\n", encoding="utf-8")


def snapshot_configs(artifacts_root: Path) -> None:
    cfg_dir = artifacts_root / "configs"
    safe_mkdir(cfg_dir)

    # Copy a few canonical config files if present (do not fail if missing)
    candidates = [
        REPO_ROOT / "docs" / "PARAMS.json",
        REPO_ROOT / "docs" / "PAPER_FIGURES_CONFIG.json",
        REPO_ROOT / "docs" / "PAPER_FIGURES_CONFIG_CORE.json",
    ]
    for p in candidates:
        if p.is_file():
            shutil.copy2(p, cfg_dir / p.name)


def snapshot_reporting(artifacts_root: Path) -> None:
    rep_dir = artifacts_root / "reporting"
    safe_mkdir(rep_dir)

    # Prefer docs/_generated tables if present
    gen_md = REPO_ROOT / "docs" / "_generated" / "EXPERIMENT_ANALYSIS_TABLES.md"
    if gen_md.is_file():
        shutil.copy2(gen_md, rep_dir / "EXPERIMENT_ANALYSIS_TABLES.md")

    # If existing summary_table.csv exists somewhere obvious, keep a copy (best-effort)
    for p in [
        REPO_ROOT / "run_aggr_strict_v2" / "artifacts" / "summary_table.csv",
        REPO_ROOT / "run_aggr_strict" / "artifacts" / "summary_table.csv",
        REPO_ROOT / "run_aggr_safe_v2" / "artifacts" / "summary_table.csv",
        REPO_ROOT / "run_aggr_safe" / "artifacts" / "summary_table.csv",
    ]:
        if p.is_file():
            shutil.copy2(p, rep_dir / "summary_table.csv")
            break

    # reporting checksums (small scope)
    compute_checksums(rep_dir, rep_dir / "checksums.sha256", exclude_names=set())


def ensure_root_readme(artifacts_root: Path) -> None:
    p = artifacts_root / "README.md"
    if p.exists():
        return
    p.write_text(
        "# Evidence Artifacts (Repo-level)\n\n"
        "This directory is a canonical, submission-friendly public evidence entry point.\n\n"
        "## Structure\n"
        "- `reporting/`: curated paper-facing exported tables, figures, and latest snapshot pointers\n"
        "- `index/`: compact pack provenance index (`run_index.csv`, `run_index.jsonl`)\n"
        "- `configs/`, `env/`: reproducibility snapshots\n"
        "- `manifest.json`: latest pack run IDs and index locations\n\n"
        "Raw `packs/` run roots are not included in this public repository. Pack origins\n"
        "are represented by `bundle_ref://...` provenance labels in `index/run_index.*`\n"
        "and by run IDs in `manifest.json`.\n\n"
        "## RUN_ID Format\n"
        "`<pack>__<tag>__<YYYYMMDD-HHMMSS>__<gitsha8>__<cfg8>`\n\n",
        encoding="utf-8",
    )


def update_root_manifest(artifacts_root: Path) -> None:
    packs_dir = artifacts_root / "packs"
    latest: Dict[str, str] = {}

    if packs_dir.is_dir():
        for pack in sorted([p for p in packs_dir.iterdir() if p.is_dir()]):
            lt = pack / "latest.txt"
            if lt.is_file():
                latest_id = lt.read_text(encoding="utf-8").strip()
                if latest_id:
                    latest[pack.name] = latest_id

    obj = {
        "schema_version": 1,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "latest": latest,
        "index": {
            "csv": "index/run_index.csv",
            "jsonl": "index/run_index.jsonl",
        },
        "notes": "Root manifest points to latest runs per pack. Each run folder contains its own manifest and checksums.",
    }
    write_json(artifacts_root / "manifest.json", obj)


def snapshot_git_state(artifacts_root: Path, gs: GitState) -> None:
    obj = {
        "commit": gs.commit,
        "branch": gs.branch,
        "dirty": gs.dirty,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
    }
    write_json(artifacts_root / "git_state.json", obj)


def run_manifest_for_pack(
    pack: str,
    run_id: str,
    tag: str,
    created_at: str,
    src_dir: Path,
    gs: GitState,
    cfg_path: Optional[Path],
    cfg_hash_full: str,
    dst_run_dir: Path,
) -> dict:
    # Basic counts / sizes
    files = [p for p in dst_run_dir.rglob("*") if p.is_file()]
    total_size = sum(p.stat().st_size for p in files)

    # Best-effort: read a few summary metrics if summary.csv exists
    summary_dict = {}
    s1 = dst_run_dir / "artifacts" / "summary.csv"
    if s1.is_file():
        try:
            # If it's a 2-column style, read as key-value; otherwise keep first row dict
            with s1.open("r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
            if rows and len(rows[0]) == 2 and all(len(r) == 2 for r in rows[:20]):
                summary_dict = {k: v for k, v in rows if k}
            else:
                with s1.open("r", encoding="utf-8") as f:
                    dr = csv.DictReader(f)
                    first = next(dr, None)
                if first:
                    summary_dict = first
        except Exception:
            summary_dict = {}

    return {
        "schema_version": 1,
        "pack": pack,
        "run_id": run_id,
        "tag": tag,
        "created_at": created_at,
        "source": {
            "src_dir": str(src_dir.relative_to(REPO_ROOT)) if src_dir.is_relative_to(REPO_ROOT) else str(src_dir),
        },
        "git": {
            "commit": gs.commit,
            "sha8": gs.sha8(),
            "branch": gs.branch,
            "dirty": gs.dirty,
        },
        "config": {
            "config_snapshot_path": (
                str(cfg_path.relative_to(REPO_ROOT)) if (cfg_path and cfg_path.is_relative_to(REPO_ROOT)) else (str(cfg_path) if cfg_path else "")
            ),
            "cfg_hash_sha256": cfg_hash_full,
            "cfg8": cfg_hash_full[:8],
        },
        "contents": {
            "file_count": len(files),
            "total_bytes": total_size,
            "has_artifacts_dir": (dst_run_dir / "artifacts").is_dir(),
            "has_figures_dir": (dst_run_dir / "figures").is_dir(),
        },
        "summary_peek": summary_dict,
    }


def collect_one_pack(
    spec: PackSpec,
    artifacts_root: Path,
    mode: str,
    dry_run: bool,
) -> Optional[str]:
    src_dir = pick_best_candidate(spec)
    if src_dir is None:
        print(f"[skip] pack={spec.name}: no candidate directories found.")
        return None

    tag = derive_tag(spec, src_dir)
    gs = GitState.detect()

    cfg_path = find_config_snapshot(src_dir)
    cfg8, cfg_full = cfg_hash8(cfg_path)

    created_at = utc_now_compact(local_tz=True)
    run_id = f"{spec.name}__{tag}__{created_at}__{gs.sha8()}__{cfg8}"

    pack_root = artifacts_root / "packs" / spec.name
    run_root = pack_root / run_id
    dst_artifacts = run_root / "artifacts"
    dst_figures = run_root / "figures"

    src_artifacts = src_dir / "artifacts"
    src_figures = src_dir / "figures"

    print(f"[pack] {spec.name}")
    print(f"  src: {src_dir.relative_to(REPO_ROOT) if src_dir.is_relative_to(REPO_ROOT) else src_dir}")
    print(f"  run: {run_id}")
    print(f"  mode: {mode}{' (dry-run)' if dry_run else ''}")

    if dry_run:
        return run_id

    # Copy/link trees
    safe_mkdir(run_root)
    copy_tree(src_artifacts, dst_artifacts, mode=mode)
    copy_tree(src_figures, dst_figures, mode=mode)

    # Run manifest + checksums
    m = run_manifest_for_pack(
        pack=spec.name,
        run_id=run_id,
        tag=tag,
        created_at=created_at,
        src_dir=src_dir,
        gs=gs,
        cfg_path=cfg_path,
        cfg_hash_full=cfg_full,
        dst_run_dir=run_root,
    )
    write_json(run_root / "manifest.json", m)
    compute_checksums(run_root, run_root / "checksums.sha256", exclude_names={"checksums.sha256"})

    # latest.txt
    safe_mkdir(pack_root)
    (pack_root / "latest.txt").write_text(run_id + "\n", encoding="utf-8")

    # Global run index update
    index_csv = artifacts_root / "index" / "run_index.csv"
    index_jsonl = artifacts_root / "index" / "run_index.jsonl"
    append_run_index(index_csv, index_jsonl, {
        "created_at": created_at,
        "pack": spec.name,
        "run_id": run_id,
        "tag": tag,
        "git_sha8": gs.sha8(),
        "cfg8": cfg_full[:8],
        "src_dir": str(src_dir.relative_to(REPO_ROOT)) if src_dir.is_relative_to(REPO_ROOT) else str(src_dir),
    })

    return run_id


def update_root_checksums(artifacts_root: Path) -> None:
    # Root checksums: keep it small/fast (exclude packs/)
    exclude_dirs = {"packs"}
    tmp_list: List[Path] = []

    for p in artifacts_root.rglob("*"):
        if p.is_dir():
            continue
        rel_parts = p.relative_to(artifacts_root).parts
        if rel_parts and rel_parts[0] in exclude_dirs:
            continue
        tmp_list.append(p)

    lines: List[str] = []
    for p in sorted(tmp_list):
        rel = p.relative_to(artifacts_root)
        h = sha256_file(p)
        lines.append(f"{h}  {rel.as_posix()}")

    (artifacts_root / "checksums.sha256").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="artifacts", help="Artifacts root directory (relative to repo root). Default: artifacts")
    ap.add_argument("--mode", default="copy", choices=["copy", "symlink", "hardlink"], help="How to place files into packs.")
    ap.add_argument("--dry-run", action="store_true", help="Print what would be done without writing.")
    ap.add_argument("--all", action="store_true", help="Collect all default packs.")
    ap.add_argument("--pack", action="append", help="Collect only specific pack(s). Can be repeated.")
    args = ap.parse_args()

    artifacts_root = REPO_ROOT / args.root

    # Determine selected packs
    if args.all:
        selected = DEFAULT_PACKS
    elif args.pack:
        wanted = set(args.pack)
        selected = [p for p in DEFAULT_PACKS if p.name in wanted]
        missing = wanted - {p.name for p in selected}
        if missing:
            print(f"[warn] unknown pack names ignored: {sorted(missing)}")
    else:
        print("Nothing selected. Use --all or --pack <name>.")
        return 2

    if not args.dry_run:
        safe_mkdir(artifacts_root)
        safe_mkdir(artifacts_root / "packs")
        safe_mkdir(artifacts_root / "index")
        ensure_root_readme(artifacts_root)

        # root snapshots (update every run; cheap)
        gs = GitState.detect()
        snapshot_git_state(artifacts_root, gs)
        snapshot_env(artifacts_root)
        snapshot_configs(artifacts_root)
        snapshot_reporting(artifacts_root)

    created: List[str] = []
    for spec in selected:
        rid = collect_one_pack(spec, artifacts_root, mode=args.mode, dry_run=args.dry_run)
        if rid:
            created.append(rid)

    if args.dry_run:
        print(f"[dry-run] would create {len(created)} run(s).")
        return 0

    # Update root manifest + checksums
    update_root_manifest(artifacts_root)
    update_root_checksums(artifacts_root)

    print(f"[done] created/updated artifacts root: {artifacts_root.relative_to(REPO_ROOT)}")
    print(f"[done] runs created: {len(created)}")
    for rid in created:
        print(f"  - {rid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
