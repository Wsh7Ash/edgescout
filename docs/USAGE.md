# Usage

## Setup

```shell
python -m pip install -e ".[dev]"
edgescout validate      # must print: edgescout: 50/50 skills valid
python -m pytest -q     # 21 passed
```

Python 3.10+, no runtime dependencies.

## Day-to-day commands

| Command | What it does |
|---|---|
| `edgescout validate` | Runs every corpus rule **and** checks `skills/**/SKILL.md` on disk against a fresh render. Exit 0 only at 50/50. |
| `edgescout validate --skip-files` | Validates the authored corpus without touching generated files (useful mid-edit). |
| `edgescout validate --json` | Machine-readable report: checked, valid, passed, floors, issues. |
| `edgescout list` | All 50 skills with their phase. |
| `edgescout list --phase audit` | Narrow to one phase (15 skills). |
| `edgescout list --tag cache-key` | Narrow to one tag. |
| `edgescout show <slug>` | Print one rendered `SKILL.md`. |
| `edgescout search <terms...>` | Rank skills by keyword across slug, title, summary, tags and steps. |
| `edgescout build` | Regenerate `skills/`, `pack.json`, `results/catalog.md` and `results/validation.json`. |

## Turning an edge profile into an audit plan

`edgeplan` reads a JSON profile of what you observed and returns a phase-ordered plan:

```shell
edgescout edgeplan --profile-file examples/demo-profile.json
edgescout edgeplan --profile-file examples/demo-profile.json --top 6 --json
```

```text
# Edge audit plan - app.example.test
Layers: 2   Unkeyed headers: 2   Skills matched: 50 of 50   Plan steps: 12   Phases covered: 6/6

Observed layers: vendor-cdn, internal-proxy
Unkeyed headers: x-original-url, x-forwarded-host

## scope

cdn-contract-inventory  (match 16)
  ...
```

Profile keys consumed as vocabulary: `hosts`, `layers`, `unkeyed_headers`, `content_classes`, `observed`, `keywords`, `questions`. Anything else in the file is ignored rather than guessed at.

- **`--top N`** caps plan length; selection is round-robin across phases, so every matched phase gets a slot before any phase gets a second.
- **Thin coverage** lists phases where the profile matched *no* skill at all. It is computed from matches, never from the truncated plan.

## Loading skills into agents

Every skill is a standalone file with YAML front-matter:

```text
skills/unkeyed-header-reflection-audit/SKILL.md
```

**Claude Code** — point `skills` at this repository in `.claude/settings.json`, or copy the directory you want into the project's skills folder:

```json
{ "skills": { "paths": ["../edgescout/skills"] } }
```

**opencode** — add the directory to `opencode.json`:

```json
{ "skill": [{ "path": "../edgescout/skills" }] }
```

Any runtime that loads `SKILL.md` files works the same way; front-matter carries `name`, `description`, `pack`, `version`, `category` and `tags`.

## Regeneration discipline

`skills/**` and `pack.json` are **generated**. Never hand-edit them — a drift test will fail.

```shell
# 1. edit the corpus in src/edgescout/corpus/part1..3.py
# 2. regenerate and check the gate
edgescout build
edgescout validate      # must print 50/50
python -m pytest -q
```

CI runs the same sequence and then `git diff --exit-code -- skills pack.json results`, so a corpus edit committed without a rebuild fails the build.
