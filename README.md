# edgescout

**50 validated edge and web-cache security skills**, plus an `edgeplan` CLI that turns an observed edge profile into a phase-ordered audit plan.

Authorized testing only: every skill in this pack describes how to *observe, confirm, harden and report* cache and CDN behaviour on systems you own or have written permission to test. The corpus contains no weaponized payload, no exploit chain and no live target data.

```shell
python -m pip install -e ".[dev]"
edgescout validate          # -> edgescout: 50/50 skills valid
edgescout build             # -> skills/, pack.json, results/
python -m pytest -q         # -> 21 passed
```

## Why this pack exists

Edge and cache defects are almost always found the same way by accident, then re-derived from scratch every time: someone notices a response looks wrong, guesses which header mattered, and never writes down the key composition they implicitly proved along the way. Meanwhile the actual preconditions — which dimensions are keyed, which headers are unkeyed, which content class may be shared — live in one engineer's memory.

`edgescout` makes that knowledge checkable. Each of the 50 skills is a single self-contained procedure with a stated **use when** and **avoid when**, a numbered procedure, observable **signals**, concrete **patterns**, known **pitfalls** and **done when** criteria. A validator enforces a quality floor on all of them and the CLI will not report success below 50/50.

## The arc

| Phase | Count | What it covers |
|---|---|---|
| `scope` | 7 | authorization boundary, consent, non-destructive probe selection, evidence hygiene |
| `fingerprint` | 8 | layer identification, cache-status vocabulary, freshness, key composition, vary, config propagation |
| `audit` | 15 | unkeyed header reflection, query/path key composition, shared storage of authenticated responses, signed assets, purge coverage, negative caching |
| `detect` | 9 | origin exposure, clean-state reproduction, cross-client confirmation, range/redirect/decode behaviour, cross-location drift |
| `harden` | 7 | explicit key policy, unkeyed input rejection, private-by-default, purge runbook, origin lockdown, drift monitoring |
| `document` | 4 | evidence pack, published reproduction, layer-aware remediation wording, coordinated disclosure |

## CLI

```shell
edgescout validate --json                 # the 50/50 gate, machine-readable
edgescout list --phase audit              # 15 skills
edgescout show cache-key-composition-probing
edgescout search vary variant
edgescout build                           # regenerate skills/, pack.json, results/
edgescout edgeplan --profile-file examples/demo-profile.json
```

### `edgeplan`

`edgeplan` is this pack's domain command. It reads a small JSON profile describing what you actually observed —

```json
{
  "target": "app.example.test",
  "hosts": ["app.example.test", "assets.example.test"],
  "layers": ["vendor-cdn", "internal-proxy"],
  "content_classes": ["public-assets", "personal-account"],
  "unkeyed_headers": ["x-original-url", "x-forwarded-host"],
  "observed": { "auth_header": "cookie" },
  "questions": ["which purge type clears keyed variants"]
}
```

— flattens it into vocabulary, scores every skill against that vocabulary, and emits an audit plan in phase order. Selection is **phase-stratified**: the first pass takes the best match in each matched phase before any phase gets a second slot, so a small `--top` can never crowd out the later phases of the arc. Phases the profile matched nothing in are reported separately as *thin coverage*, which is computed from matches rather than from the truncated plan.

## Loading the skills into an agent runtime

Each skill is a standalone `skills/<slug>/SKILL.md` with YAML front-matter, so any runtime that loads `SKILL.md` files can use them directly:

```text
skills/
├─ scope/…   (front-matter carries pack, version, category and tags)
├─ …
```

Claude Code and opencode both discover them from a skills directory; see [docs/USAGE.md](docs/USAGE.md) for the exact configuration.

## Layout

```text
src/edgescout/
├─ corpus/        authored skill data — the single source of truth
│  ├─ part1.py    skills 1-15   (scope, fingerprint)
│  ├─ part2.py    skills 16-30  (audit)
│  └─ part3.py    skills 31-50  (detect, harden, document)
├─ model.py       Skill dataclass + strict dict loading
├─ render.py      deterministic SKILL.md / pack.json / results writer
├─ validate.py    every rule, one place
└─ cli.py         validate / list / show / search / build / edgeplan
```

Markdown files under `skills/` are **generated**. Edit the corpus, run `edgescout build`, and a test asserts the committed files match a fresh render — the two can never silently disagree.

## Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — components, data flow, design decisions
- [docs/USAGE.md](docs/USAGE.md) — commands, agent integration, regeneration discipline
- [docs/PROJECT_SPEC.md](docs/PROJECT_SPEC.md) — problem, solution, acceptance tests
- [RESULTS.md](RESULTS.md) — reproducible evidence for every claim above
- [SECURITY.md](SECURITY.md) — authorized-use scope and the reporting path
- [CONTRIBUTING.md](CONTRIBUTING.md) — the quality floor CI enforces

## License

MIT. References link to public specifications and vendor documentation; see each skill's **References** section.
