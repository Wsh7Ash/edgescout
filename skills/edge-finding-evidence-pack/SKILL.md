---
name: edge-finding-evidence-pack
description: "Assemble a report where every edge claim carries the request pair, the cache status tokens and the timestamps that prove it. Use when an edge or cache observation is ready to be written up for the owner or a vendor"
pack: edgescout
version: 1.0.0
category: web-app
tags: [document, evidence, reporting]
---

# Edge Finding Evidence Pack

> Assemble a report where every edge claim carries the request pair, the cache status tokens and the timestamps that prove it

**Use when:** an edge or cache observation is ready to be written up for the owner or a vendor

**Avoid when:** the finding has already been reported and only a closing note remains

## Procedure

1. State the defect in one sentence that names the layer, the dimension and the outcome, without adjectives.
2. Attach the pairing log: the two or three requests whose only difference was the dimension at issue.
3. Include cache status tokens, age values and the relevant directives for each request in the pair.
4. Record the timestamps so a reader can tell which observation came before another.
5. Give the reproduction recipe from clean state and the boundary document version that permitted each request.
6. State the realistic impact in terms of what a normal client would observe, and keep speculation out of it.

## Signals

- A report claims a cache defect without showing the request pair that revealed it
- Status tokens are missing from the evidence, leaving stored versus live ambiguous
- Observations have no timestamps, so the order of events cannot be established
- Impact is described in hypothetical terms no tested request supports

## Patterns

**1. Claim skeleton**

```text
claim: <layer> stores <content> keyed without <dimension>
pair: request A / request B, differing only in <dimension>
tokens: <status on each>
impact: <what a normal client sees>
```

**2. Evidence block**

```text
2026-05-11T09:12Z GET /path (no header) -> 200 hit age=118
2026-05-11T09:12Z GET /path (header X)  -> 200 hit age=0
2026-05-11T09:13Z GET /path (no header) -> 200 hit age=0 body changed
```

**3. Boundary note**

```text
attach the boundary document version and mark each request as permitted by it, so a reviewer can audit the test itself
```

## Pitfalls

- Presenting a narrative claim when the reader needs the raw request pair to judge it
- Leaving out the layer attribution, so the owner cannot route the report to the right team
- Inflating impact beyond what the recorded requests demonstrate

## Done when

- Every claim in the report is followed by a request pair with status tokens and timestamps
- The reproduction recipe and boundary version are attached to the pack

## References

- [OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-61 - Incident handling guidance](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
