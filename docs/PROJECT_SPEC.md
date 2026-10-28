# Project Spec — edgescout

## Name

`edgescout`

## Category

`web-app`

## Target user

Security engineers, bug-bounty hunters and agents performing **authorized** assessment of properties that sit behind a CDN, reverse proxy or other shared cache.

## Problem

Edge and cache methodology is scattered across vendor documentation, conference talks and post-mortems. Each new assessment re-decides the same things from scratch: which request dimensions actually form the cache key, which untrusted headers sit outside it, what the vendor's status vocabulary means, whether a response may be stored in a shared cache at all, how to confirm a leak without reading a third party's data, and which layer owns each fix. None of it is machine-checkable, and agents have no structured skill files to load — so every engagement reinvents a procedure that already exists in someone else's head.

## Solution

A corpus of 50 unique, validated edge and web-cache skills organised into the six phases of an assessment (`scope`, `fingerprint`, `audit`, `detect`, `harden`, `document`), a validator that enforces quality floors, and an `edgeplan` CLI that turns an observed edge profile into a phase-ordered audit plan with honest thin-coverage reporting.

## Core workflow

```text
author/edit corpus  ->  build  ->  skills/ + pack.json + results/
                                    |
                                    v
                          validate (50/50 gate)  ->  pytest  ->  CI
                                    |
                                    v
                       edgeplan --profile-file profile.json -> ordered plan
```

## Must-have features

- 50 unique skills with unique slugs and titles across the six phases.
- Validator with structural, strength and hygiene rules; exit `0` only at 50/50.
- Deterministic renderer; committed files proven in sync by tests.
- `edgeplan` producing a phase-ordered plan from a JSON observation profile, with thin coverage derived from matches rather than from the truncated plan.

## Nice-to-have (explicitly out of scope for v1)

- Live network probing. The pack deliberately makes **no** network requests.
- Automatic key inference from captured traffic.
- Vendor-specific configuration generation.

## Acceptance tests

1. `validate` exits 0 and reports 50/50.
2. `pytest -q` passes 21 tests, including regeneration equality and drift detection.
3. `edgeplan` — round-trips the checked-in example profile, covers all 6 phases with `--top 6`, and reports no thin coverage for a profile that matches everything.
4. A generated build lands byte-identically in a clean temp directory.

## Authorized-use constraint

This is a defensive and methodology pack. Skills describe observation, confirmation, hardening and disclosure. The corpus contains no exploit payloads, no weaponized proof-of-concept and no live target data; `SECURITY.md` states the boundary and the reporting path.
