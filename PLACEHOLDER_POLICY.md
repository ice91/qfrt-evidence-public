# PLACEHOLDER_POLICY

This policy defines how `TODO_PUBLIC_PLACEHOLDER://...` values are interpreted in
this public repository.

## 1) Purpose

`TODO_PUBLIC_PLACEHOLDER://...` marks an intentionally unresolved reference in a
public-safe configuration or mapping file.

It is used when:

- a direct runtime/internal source path should not be exposed,
- a concrete public artifact path is not yet fixed,
- the repository must remain portable and non-environment-specific.

## 2) Interpretation rule

For a value like:

`TODO_PUBLIC_PLACEHOLDER://artifacts/reporting/figure_inputs/appA_results.csv`

interpretation is:

- `TODO_PUBLIC_PLACEHOLDER://` = unresolved public-safe marker
- trailing path = intended repo-local target shape when/if resolved

The trailing path is descriptive guidance, not a guaranteed existing file.

## 3) Allowed usage

Allowed in:

- public config files
- public mapping/index metadata where unresolved references are explicit

Not intended for:

- executable runtime path resolution without a pre-resolution step
- hiding mandatory dependencies that are required to read curated artifacts

## 4) Resolution options at release time

A placeholder can be handled in one of two acceptable ways:

1. **Resolve** to a concrete repo-local path if the file is included.
2. **Retain** as placeholder and document it in release notes/checklists.

Either option must preserve transparent reviewer interpretation.

## 5) Current inventory (candidate freeze)

Current `TODO_PUBLIC_PLACEHOLDER://...` entries are in:

- `docs/PAPER_FIGURES_CONFIG_CORE.json`
  - `appA_results_csv`
  - `appD_omega1d_summary_csv`
  - `appE_real_capture_csv`
- `artifacts/configs/PAPER_FIGURES_CONFIG_CORE.json`
  - `appA_results_csv`
  - `appD_omega1d_summary_csv`
  - `appE_real_capture_csv`

