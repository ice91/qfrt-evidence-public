# PUBLIC_RELEASE_CANDIDATE_CHECKLIST

Use this checklist to validate release readiness of the public evidence repository.

## A. Public-surface wording

- [x] Public-facing explainer avoids runtime command dependencies.
- [x] Config language avoids non-public policy wording.
- [x] Script headers declare optional-helper status where runtime assumptions may exist.

## B. Path hygiene

- [x] Figure config paths no longer point to `benchmark_suite/...`.
- [x] Placeholder references are explicit and reviewable.
- [x] Public docs and manifest/index surfaces remain repo-local or placeholder-based.

## C. Technical anchor consistency

- [x] Public docs align with artifact-first / evidence-first posture.
- [x] Parameter notes are neutral and externally publishable.
- [x] Export-helper scripts are clearly separated from full execution pipeline semantics.

## D. Pre-release quick checks

- [ ] Optional: run a final keyword sweep for runtime-specific command strings.
- [ ] Optional: verify placeholder paths are either resolved or documented in release notes.
- [ ] Optional: update checksum snapshots if release packaging requires strict integrity freeze.

