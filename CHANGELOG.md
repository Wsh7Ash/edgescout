# Changelog

All notable changes to `edgescout` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [1.0.0] - 2026-10-28

### Added

- Initial release: 50 unique edge and web-cache security skills across six phases
  (`scope`, `fingerprint`, `audit`, `detect`, `harden`, `document`).
- Validator with structural, strength and hygiene rules; `50/50 skills valid`
  gate with `--json` output for CI.
- Deterministic renderer and `build` command writing `skills/`,
  `pack.json` (SHA-256 per skill) and `results/`.
- CLI: `validate`, `list`, `show`, `search`, `build`, `edgeplan`.
- `edgeplan` — observed edge profile to phase-ordered audit plan, with
  phase-stratified selection and match-derived thin-coverage reporting.
- Example profile `examples/demo-profile.json`.
- Test suite (21 tests) covering corpus shape, rules, regeneration, drift,
  every CLI command and edgeplan's selection semantics.
- CI workflow, docs (`ARCHITECTURE`, `USAGE`, `PROJECT_SPEC`), `SECURITY.md`.

### Design notes

- `missing_phases` is derived from matched skills, not from the plan truncated
  by `--top`, so a covered phase can never be reported as uncovered.
- Selection draws matches round-robin across `PHASE_ORDER` before any phase
  receives a second slot, so `--top 6` still covers all six phases when the
  profile matches them.
