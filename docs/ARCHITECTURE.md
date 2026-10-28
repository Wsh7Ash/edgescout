# Architecture

## Goals

1. **One source of truth.** Skills are authored as Python data; Markdown files are generated. A test asserts committed files match a fresh render, so the two can never disagree.
2. **Validation is a first-class gate.** Every quality floor lives in `validate.py` and is enforced by both the CLI and the test suite.
3. **No runtime dependencies.** Standard library only, so the pack runs anywhere Python 3.10+ exists.

## Components

```text
src/edgescout/
├─ corpus/           authored skill data (source of truth)
│  ├─ __init__.py    PACK metadata, PHASE_ORDER + loads part1..part3
│  ├─ part1.py       skills 1-15   (scope, fingerprint)
│  ├─ part2.py       skills 16-30  (audit)
│  └─ part3.py       skills 31-50  (detect, harden, document)
├─ model.py          Skill dataclass + strict dict loading
├─ render.py         deterministic SKILL.md + pack.json + results writer
├─ validate.py       every rule, one place
└─ cli.py            validate / list / show / search / build / edgeplan
```

### Data flow

```text
part1..part3 (dicts)
      │  skill_from_dict()  -- shape check, rejects missing/empty fields
      ▼
   Skill (frozen dataclass)
      │
      ├─ validate_pack()  ─▶ Issue list ─▶ CLI exit code (0 only at 50/50)
      └─ render_skill()   ─▶ skills/<slug>/SKILL.md  (byte-deterministic)

profile.json ─▶ profile_vocabulary() ─▶ build_edgeplan()
                                          │  phase-stratified selection
                                          ▼
                        phase-ordered plan + thin-coverage phase list
```

### The edgeplan command

`edgeplan` is edgescout's domain command and separates this pack from a document library. It consumes a small profile of what the tester *observed* — hosts, edge layers, unkeyed headers, content classes, plus free-text questions — and flattens it into lowercase tokens. Every skill is scored by counting how many of those tokens appear in its slug, title, summary, tags and steps.

Selection is then **phase-stratified**: matches are bucketed by phase, sorted by score, and drawn round-robin in `PHASE_ORDER`. Round 0 takes the best match from every matched phase, round 1 the second-best, and so on until `--top` is reached. Two consequences:

- a small `--top` (even `top=6`) still yields one step from every phase the profile matched;
- ordering inside the output still follows the arc, so the plan reads scope → fingerprint → audit → detect → harden → document.

`missing_phases` is computed from **matched** skills, not from the truncated plan. This is deliberate: reporting "no matched skill in these phases" for a phase that matched but was cut by `--top` would be a false statement, and it is exactly the sort of silent gap the pack exists to make visible.

### Design decisions

- **`edgeplan` stays vocabulary matching.** It encodes "what did you observe → what should you look at", not an assessment policy engine. Judgement about which observation matters belongs to the reader; the CLI's job is to surface phases that would otherwise be skipped.
- **Phases are data, not code.** `PHASE_ORDER` lives in `corpus/__init__.py` next to `PACK`, so the renderer, the validator, the CLI and the tests all read the same tuple. Adding a phase means editing one tuple plus its skills.
- **Generated files are never hand-edited.** `validate` compares every `skills/**/SKILL.md` byte-for-byte against a fresh render and fails on drift, which is why CI can run `build` followed by `git diff --exit-code`.
- **`meta` is open-ended.** `PACK["meta_keys"]` declares which meta fields are required; `edgeplan` only needs `phase`. Another pack on the same harness can require `cwe` or `threat_id` without touching the model.

## Test surface

`tests/test_corpus.py` covers corpus shape (counts, uniqueness, phase balance), every validation rule, regeneration equality, drift detection, every CLI subcommand including `edgeplan`'s stratified selection and thin-coverage semantics, and the integrity of the committed `pack.json` hashes and `results/` reports.
