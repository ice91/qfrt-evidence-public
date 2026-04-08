# Paper Figures / Tables Mapping (Public Evidence View)

This document maps candidate figure/table artifacts to manuscript sections,
using only curated, portable references.

## Mapping policy

- Prefer curated reporting tables in `artifacts/reporting/`.
- Use `artifacts/reporting/paper_runs/latest.txt` for the latest public
  assembled paper-run figure/table snapshot.
- Use `artifacts/reporting/phase1_regime_boundary/latest.txt` only for the
  exploratory Phase I boundary bundle.
- If figure assets are unavailable in this public surface, keep table-backed
  evidence and mark figure slot as TODO.
- Avoid assumptions about local runtime-generated directories.

## Candidate evidence blocks

1. Stability summary
2. Two-layer gain summary
3. Low-z onset interval summary
4. SNR robustness summary
5. Mask robustness summary (validated runs only)

## Notes for manuscript rewrite

- Use interval language for onset-related statements.
- Keep robustness wording conservative and range-bounded.
- If a figure depends on unavailable runtime output, cite the corresponding
  curated table and mark figure generation as deferred.
