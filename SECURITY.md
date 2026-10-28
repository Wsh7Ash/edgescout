# Security Policy

## Authorized use only

`edgescout` is a knowledge corpus and planning tool for **authorized** security work: assessing properties you own, or programs whose rules explicitly permit the testing you perform. The software itself performs **no network requests** — it renders, validates and plans locally from a JSON profile you supply.

The skills describe edge and cache **assessment** methodology: how to fingerprint a layer, which dimensions form a cache key, how to confirm that one client received another's stored response without reading that content, and how to fix and disclose what you found. They contain no weaponized exploit material.

## What this corpus deliberately does not contain

- No exploit payloads, proof-of-concept attack code or automation against third parties.
- No instructions for accessing a system without written authorization.
- No credential harvesting, session theft, phishing or evasion guidance.
- No live target data, credentials or personal data. The example profile (`examples/demo-profile.json`) uses `example.test` names and synthetic values only.

## Scope discipline is built into the corpus

The opening skills exist to keep an assessment bounded and honest:

1. `authorization-boundary-documentation` — the written boundary is re-read before the first request of every session.
2. `personal-data-cache-scope` — shared-cache behaviour is never exercised against real user records; only synthetic accounts the tester owns.
3. `evidence-hygiene-for-cached-responses` — a hash proves sameness without archiving a body that contains someone else's data.
4. `non-destructive-probe-selection` — verbs and dimensions vary one at a time, and state-changing methods stay out of the default plan.

`edgeplan` always emits `scope` first for this reason: a plan that begins with an observation rather than a permission is a plan that has already skipped its most important step.

## Reporting a vulnerability in this project

If you find a defect in `edgescout` itself — for example, a validation bypass that lets a malformed skill pass the 50/50 gate — please open a private security advisory on the repository or contact the maintainer through GitHub. Do not publish exploit details before a fix is available.

## Scope of this project's own testing

All tests run locally against the checked-in corpus and the checked-in example profile. No test sends traffic anywhere; `edgeplan` reads one JSON file and scores text. Continuous integration runs the same local gates: validation, unit tests and an artifact-sync check.
