# RELEASE_READINESS_REPORT

Date: 2026-04-02

## Overall assessment

Status: **not release-ready yet**.

The repository is close to a public technical-anchor posture, but there are still
documented release blockers and several metadata inconsistencies that should be
resolved before a public release.

## 1) Wording inconsistencies

1. License posture is contradictory.
   - [README.md](/Users/rocky/qfrt-evidence-public/README.md#L57) says the repo does not choose or imply a final public license.
   - [LICENSE](/Users/rocky/qfrt-evidence-public/LICENSE#L1) already declares BSD 3-Clause.
   - [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L17) says `NOASSERTION`.
   - This is the clearest cross-file inconsistency and should be treated as a release blocker.

2. Blocker status is inconsistent across release documents.
   - [RELEASE_NOTES.md](/Users/rocky/qfrt-evidence-public/RELEASE_NOTES.md#L17) says blocker cleanup was completed.
   - [FINAL_RELEASE_QUICKCHECK.md](/Users/rocky/qfrt-evidence-public/FINAL_RELEASE_QUICKCHECK.md#L18) says there are no newly introduced blockers.
   - [RELEASE_BLOCKERS_REMAINING.md](/Users/rocky/qfrt-evidence-public/RELEASE_BLOCKERS_REMAINING.md#L5) still lists unresolved high-priority and medium-priority blockers.
   - Those statements cannot all be true at the same time.

3. The repository role is described with slightly different emphasis across files.
   - [README.md](/Users/rocky/qfrt-evidence-public/README.md#L3) uses “technical anchor for evidence review”.
   - [AVAILABILITY.md](/Users/rocky/qfrt-evidence-public/AVAILABILITY.md#L5) uses “technical anchor” plus “configuration snapshots”.
   - [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L9) uses “curated, review-facing technical package”.
   - This is not blocking, but a tighter shared phrase would improve release consistency.

4. The execution-boundary language is not fully normalized.
   - [README.md](/Users/rocky/qfrt-evidence-public/README.md#L11) says it is not the execution environment.
   - [README.md](/Users/rocky/qfrt-evidence-public/README.md#L25) uses “runtime contract”.
   - [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L38) uses “execution workspace”.
   - [RELEASE_NOTES.md](/Users/rocky/qfrt-evidence-public/RELEASE_NOTES.md#L25) uses “full experiment execution workspace”.
   - The intent is consistent, but the wording varies enough that one public-safe formulation should be chosen and reused.

## 2) Remaining implementation-forward or private-core-forward phrasing

These phrases do not expose private implementation directly, but they still lean
more implementation-forward than needed for a public technical anchor.

1. [AVAILABILITY.md](/Users/rocky/qfrt-evidence-public/AVAILABILITY.md#L6) says “configuration snapshots”.
   - “Configuration” pushes the repo slightly toward execution internals. “Artifact interpretation metadata” or similar would be more anchor-oriented.

2. [AVAILABILITY.md](/Users/rocky/qfrt-evidence-public/AVAILABILITY.md#L21) says “non-public implementation systems”.
   - This is accurate, but it foregrounds private implementation instead of simply defining the public boundary.

3. [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L13) uses a section named “Configs”.
   - That section reads closer to system packaging than evidence presentation.

4. [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L29) explicitly says “Private core implementation”.
   - This is boundary-setting language, but it still centers the private core more than necessary.

5. [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L31) says “Benchmark execution engine” and mentions “orchestration stack” and “runtime-only pipelines”.
   - This is implementation-forward vocabulary for a public-facing scope document.

6. [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L57) is titled “Data retained in private repositories”.
   - Again, it is public-safe, but it keeps attention on private surfaces rather than the public artifact boundary.

7. [README.md](/Users/rocky/qfrt-evidence-public/README.md#L56) says “unresolved runtime dependency”.
   - For a repository that is intentionally not a runtime environment, this phrasing suggests dependency semantics that the README otherwise tries to avoid.

8. [RELEASE_NOTES.md](/Users/rocky/qfrt-evidence-public/RELEASE_NOTES.md#L11) says “Public-safe config snapshots”.
   - This is acceptable, but still more implementation-oriented than “artifact interpretation metadata” or “supporting metadata”.

## 3) Missing or incorrect public-release metadata

1. `CITATION.cff` repository URL appears malformed.
   - [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L8) points to `https://github.com/ice91/qfrt-evidence-public/qfrt-evidence-public`.
   - GitHub repository URLs normally end at `owner/repo`. The duplicated repo segment looks incorrect.
   - This is a release blocker because it breaks citation/discovery metadata.

2. `CITATION.cff` license metadata does not match the repository license.
   - [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L17) is `NOASSERTION`.
   - [LICENSE](/Users/rocky/qfrt-evidence-public/LICENSE#L1) is BSD 3-Clause.
   - This is a release blocker because citation metadata should agree with the published license.

3. The release metadata does not clearly identify a canonical public release locator.
   - [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L18) has a version string and [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L19) has a release date.
   - [TECHNICAL_ANCHOR_SCOPE.md](/Users/rocky/qfrt-evidence-public/TECHNICAL_ANCHOR_SCOPE.md#L50) recommends immutable revision identifiers.
   - There is no explicit release URL, tag reference, or DOI metadata in the citation file.
   - This may be acceptable for an internal candidate freeze, but it is incomplete for a polished public release.

4. README release-policy wording is outdated relative to the current files.
   - [README.md](/Users/rocky/qfrt-evidence-public/README.md#L57) says the repo does not choose or imply a final public license.
   - Once a `LICENSE` file is present, that sentence is stale metadata, not just phrasing.

5. Authorship metadata may need confirmation for public citation quality.
   - [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L5) uses one author entry with `family-names: "QFRT Team"` and `given-names: "Research"`.
   - This may validate syntactically, but it reads like a placeholder-style organizational author rather than finalized citation metadata.
   - Not necessarily blocking, but worth confirming before release.

## 4) Release blockers

1. Active blocker file still lists unresolved high-priority issues.
   - [RELEASE_BLOCKERS_REMAINING.md](/Users/rocky/qfrt-evidence-public/RELEASE_BLOCKERS_REMAINING.md#L7) still flags public docs/config files with runtime-command, `PPA`, `Claim`, and `benchmark_suite/...` references.
   - Given the repository goal and AGENTS constraints, this alone means the repo should not yet be called fully public-release-ready.

2. License metadata is internally inconsistent.
   - [LICENSE](/Users/rocky/qfrt-evidence-public/LICENSE#L1), [README.md](/Users/rocky/qfrt-evidence-public/README.md#L57), and [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L17) disagree on whether a public license is finalized.

3. Citation repository URL is likely wrong.
   - [CITATION.cff](/Users/rocky/qfrt-evidence-public/CITATION.cff#L8) should be corrected before release.

4. Release-governance documents disagree on readiness.
   - [RELEASE_NOTES.md](/Users/rocky/qfrt-evidence-public/RELEASE_NOTES.md#L17), [FINAL_RELEASE_QUICKCHECK.md](/Users/rocky/qfrt-evidence-public/FINAL_RELEASE_QUICKCHECK.md#L18), and [RELEASE_BLOCKERS_REMAINING.md](/Users/rocky/qfrt-evidence-public/RELEASE_BLOCKERS_REMAINING.md#L5) currently send conflicting signals.
   - A public release should present one authoritative readiness state.

## Recommended disposition

Do not publish as a final public release yet.

Minimum actions before release:

1. Resolve the license inconsistency across `LICENSE`, `README.md`, and `CITATION.cff`.
2. Fix the `repository-code` URL in `CITATION.cff`.
3. Reconcile `RELEASE_NOTES.md`, `FINAL_RELEASE_QUICKCHECK.md`, and `RELEASE_BLOCKERS_REMAINING.md` so blocker status is unambiguous.
4. Remove or soften implementation-forward wording in the public-facing docs, especially references to configs, private core implementation, orchestration, runtime pipelines, and execution engines where simpler boundary language would work.
