# Reviewer Checklist (Public Evidence Repository)

This checklist is for reviewing the curated evidence surface in this repository.

## A. Repository-surface checks

- [ ] Paths are repo-local and portable
- [ ] No absolute machine-specific paths in docs/manifests/index
- [ ] No unresolved runtime assumptions without TODO markers

## B. Evidence validity checks

- [ ] Stability summary present
- [ ] Two-layer gain summary present
- [ ] Low-z onset summary presented as interval
- [ ] SNR summary phrased as robust but attenuating (range-bounded)
- [ ] Mask summary uses validated runs only (invalid runs excluded)

## C. Claim-boundary checks

- [ ] No sharp-threshold phrasing when only interval evidence exists
- [ ] No universal-law wording beyond tested ranges
- [ ] Any missing evidence source is explicitly marked as TODO/placeholder

## D. Provenance checks

- [ ] `artifacts/index/` is readable and consistent
- [ ] `artifacts/manifest.json` points to repo-local references
- [ ] reporting tables referenced in docs exist in `artifacts/reporting/`

## E. Release-hygiene checks

- [ ] Sensitive wording is neutralized in public-facing docs
- [ ] Unsupported execution dependencies are removed from docs
- [ ] Curated evidence remains interpretable without non-local runtime context

