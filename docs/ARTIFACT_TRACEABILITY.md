# Artifact Traceability (Public Evidence Surface)

This document defines how curated evidence files in this repository map to
portable, review-facing artifacts.

## Principles

1. **Artifact-first**: primary objects are frozen tables, summaries, and manifest metadata.
2. **Portable paths**: references must be repo-local relative paths.
3. **Lightweight provenance**: index + manifest should be sufficient for navigation.
4. **No runtime assumptions**: avoid requiring execution stack details in this repo.

## Traceability layers

- Layer A: `artifacts/reporting/`
  - curated review-facing outputs
- Layer B: `artifacts/index/`
  - run-level index metadata
- Layer C: `artifacts/manifest.json`
  - latest pointers and schema info

## Path policy

Allowed:

- repo-local relative paths (e.g., `artifacts/reporting/...`)
- explicit TODO placeholders for unresolved external references

Not allowed:

- absolute machine paths
- parent traversal assumptions that break portability
- environment-specific hardcoded run output roots

## Integrity policy

- Keep checksums for reporting/index surfaces where available.
- If checksum scope is incomplete, annotate as TODO and avoid silent assumptions.

## Review checklist

- [ ] all key references are repo-local
- [ ] no absolute path assumptions
- [ ] unresolved sources marked as TODO/placeholder
- [ ] curated tables map cleanly to evidence statements

