# REMAINING_NONBLOCKING_ITEMS

These items are non-blocking for this targeted cleanup pass but may be improved in a future polish pass.

## 1) Script internals still contain runtime-oriented identifiers

- Some variable names and internal comments in `scripts/*.py` still use run/pack naming conventions.
- Current status is acceptable because this pass only required public-safe top-level framing without changing behavior.

## 2) Placeholder resolution policy

- `TODO_PUBLIC_PLACEHOLDER://...` values are intentionally unresolved.
- A future release note can define whether they should be mapped to concrete repo-local files or remain explicit TODO placeholders.

## 3) Legacy artifacts under reporting snapshots

- Historical `paper_runs/*` content still contains run IDs and historical structure names.
- These are retained for provenance continuity and were not requested for mutation in this targeted pass.

## 4) Optional consistency pass

- If a stricter release gate is desired, run one final whole-repo wording/path audit and decide whether to sanitize additional non-target docs.

