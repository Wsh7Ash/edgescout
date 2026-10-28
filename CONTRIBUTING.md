# Contributing

Thanks for helping improve `edgescout`.

## Ground rules

- **Authorized-use scope only.** Contributions must stay defensive or methodology-focused: no weaponized payloads, no exploit chains, no instructions for accessing systems the reader does not own or have written permission to test.
- **No live data.** Never commit real target names, hostnames, credentials, cookies, tokens or personal data. Synthetic examples only — `example.test` names and invented values.
- **One skill, one job.** A skill must be a single self-contained procedure with a clear "use when" and "avoid when".
- **No network calls.** The package stays stdlib-only and offline at runtime.

## Adding or editing a skill

1. Edit the corpus in `src/edgescout/corpus/part1.py`–`part3.py` (the source of truth). Do **not** hand-edit `skills/**/SKILL.md`; generated files are overwritten and a drift test will fail.
2. Regenerate and check the gate:

   ```shell
   edgescout build
   edgescout validate   # must print 50/50
   python -m pytest -q
   ```

3. Keep counts honest: adding a skill to the pack requires removing or merging another to keep the corpus at 50, or raising `expected_skills` deliberately in `corpus/__init__.py` together with a note in the PR.
4. If you add a phase, extend `PHASE_ORDER` in `corpus/__init__.py` and update the phase assertions in `tests/test_corpus.py` in the same change.

## Quality floor enforced by CI

| Rule | Floor |
|---|---|
| Steps / signals / patterns / pitfalls / done-when | 6 / 4 / 3 / 3 / 2 |
| Rendered words per skill | >= 180 |
| References | canonical `[label](https://...)`, >= 1 |
| Slugs and titles | unique, lowercase kebab-case |
| Summary / use-when / avoid-when | >= 40 / 30 / 30 chars |
| Description (front-matter) | 120-1024 chars |
| Hygiene | no placeholder tokens, no machine-local paths |

## Pull requests

- Keep one concern per PR (one skill family, one rule change, one CLI feature).
- Include the output of `validate` and `pytest` in the description.
- Update `CHANGELOG.md` and `RESULTS.md` when behaviour changes.
