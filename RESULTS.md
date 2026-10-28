# Results

Reproducible evidence for the claims in `README.md`.

## Environment

- OS: Windows (MSYS2 shell)
- Python: 3.14.3 (`requires-python >= 3.10`)
- Runtime dependencies: none (standard library only)
- Dev dependency: `pytest`
- Network: none required at any point — the package performs no network requests

## Validation performed

### 1. Corpus gate — PASS

```shell
$ PYTHONPATH=src python -m edgescout validate --json
{
  "pack": "edgescout",
  "checked": 50,
  "valid": 50,
  "passed": true,
  "floors": {
    "min_steps": 6,
    "min_signals": 4,
    "min_patterns": 3,
    "min_pitfalls": 3,
    "min_done_when": 2,
    "min_summary_chars": 40,
    ...
```

```shell
$ PYTHONPATH=src python -m edgescout validate
edgescout: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Exit code 0. With generated files included (the default), this also byte-compares every `skills/**/SKILL.md` against a fresh render.

### 2. Test suite — PASS (21 tests)

```shell
$ PYTHONPATH=src python -m pytest -q
.....................                                                    [100%]
21 passed
```

Covered: pack declares and delivers 50; slugs and titles unique; every skill passes every rule; all six phases populated and balanced; word floor holds on the weakest skill; no placeholder or machine-local path tokens; committed `SKILL.md` files match the render; `pack.json` hashes match file bytes; build is byte-idempotent in a temp directory; drift is detected; `validate --json` reports 50/50; `list`/`show`/`search` behave as documented; `edgeplan` orders phases, covers all six with `--top 12`, rejects a missing profile, aggregates vocabulary across profile keys, and reports thin coverage from matches rather than from the truncated plan; `results/validation.json` and `results/catalog.md` are consistent with the corpus.

### 3. Build and artifact sync — PASS

```shell
$ PYTHONPATH=src python -m edgescout build
built 50 skills -> .../edgescout/skills
$ PYTHONPATH=src python -m edgescout validate
edgescout: 50/50 skills valid
```

Regenerating twice produces byte-identical output; `test_build_is_idempotent` asserts this against a clean temp directory.

### 4. Phase distribution — as specified

```shell
$ PYTHONPATH=src python -m edgescout list | tail -1
-- 50 skills
$ PYTHONPATH=src python -m edgescout list --phase audit | tail -1
-- 15 skills
```

| Phase | Skills |
|---|---|
| scope | 7 |
| fingerprint | 8 |
| audit | 15 |
| detect | 9 |
| harden | 7 |
| document | 4 |
| **total** | **50** |

### 5. `edgeplan` on the checked-in example — PASS

```shell
$ PYTHONPATH=src python -m edgescout edgeplan --profile-file examples/demo-profile.json
# Edge audit plan - app.example.test
Layers: 2   Unkeyed headers: 2   Skills matched: 50 of 50   Plan steps: 12   Phases covered: 6/6

Observed layers: vendor-cdn, internal-proxy
Unkeyed headers: x-original-url, x-forwarded-host

## scope

cdn-contract-inventory  (match 16)
  Establish which caching layer is contracted to do what, so an unexpected behaviour is measured against the documented configuration rather than a guess
   1. Ask the owner for the current edge vendor list, zone file or DNS records showing which hostnames route through which provider.
   ...
```

Observed behaviour: 50 of 50 skills matched the profile vocabulary; the plan contains 12 steps spread across **all 6 phases** despite `--top 12`; `missing_phases` is empty because every phase matched.

### 6. Ranking sanity — PASS

```shell
$ PYTHONPATH=src python -m edgescout search vary variant --limit 3
 12  vary-variant-mapping                         Vary Variant Mapping
  8  content-negotiation-key-dimensions           Content Negotiation Key Dimensions
  6  decode-order-mismatch-detection              Decode Order Mismatch Detection
```

The intended skill ranks first for its own vocabulary.

## Commands executed

```shell
python -m edgescout validate --json
python -m edgescout validate
python -m edgescout build
python -m edgescout list --phase audit
python -m edgescout search vary variant --limit 3
python -m edgescout edgeplan --profile-file examples/demo-profile.json
python -m pytest -q
```

## Known limitations

- **`edgeplan` is vocabulary matching, not an assessment engine.** It scores observed tokens against skill text. It will not tell you which observation matters most, only which skills relate to what you saw and which phases you matched nothing in.
- **Thin coverage is only as good as the profile.** A profile missing a layer that exists in the estate cannot report that layer's phase as thin.
- **No network probing.** Nothing in this pack captures traffic, infers keys from recordings, or contacts a target. Key composition still has to be established by the tester and written into the profile.
- **Verification of a fix is manual.** The pack tells you which retest to run; it does not run it.
- Tests were run on Python 3.14 locally. CI additionally covers 3.10, 3.12 and 3.13.

## Generated artifacts

| Path | What it is |
|---|---|
| `skills/**/SKILL.md` | 50 rendered skills, byte-identical to the corpus |
| `pack.json` | manifest with SHA-256 per skill file |
| `results/catalog.md` | generated skill catalog table |
| `results/validation.json` | machine-readable gate report (`passed: true`) |
| `examples/demo-profile.json` | the example edge profile used above |