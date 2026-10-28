---
name: evidence-hygiene-for-cached-responses
description: "Record edge behaviour without archiving response bodies that may contain personal or session-bound data, keeping the evidence package safe to share with the vendor. Use when collecting responses during an edge assessment where any recorded body might contain account data, tokens or tenant content"
pack: edgescout
version: 1.0.0
category: web-app
tags: [evidence, privacy, reporting]
---

# Evidence Hygiene for Cached Responses

> Record edge behaviour without archiving response bodies that may contain personal or session-bound data, keeping the evidence package safe to share with the vendor

**Use when:** collecting responses during an edge assessment where any recorded body might contain account data, tokens or tenant content

**Avoid when:** the entire test surface is public static content that the owner has cleared for full archiving

## Procedure

1. Record request line, status, timing and the full caching header set for every observation before considering body capture.
2. Capture bodies only for synthetic content you own, and redact any value that resembles a token, cookie or account identifier first.
3. For personal-class responses, store a SHA-256 of the body plus its length instead of the body itself, so sameness can still be proven.
4. Keep a numbered index linking each evidence line to the boundary document version and the probe that produced it.
5. Store raw header dumps separately from the narrative report so a reviewer can re-check claims without reading prose.
6. Delete transient captures once the report is filed, keeping only what the disclosure record requires.

## Signals

- An evidence folder contains responses from accounts the tester does not own
- Recorded headers include a session cookie or bearer token in clear text
- The same account data appears in several unrelated evidence files
- A report draft embeds a full response body where a hash would prove the point

## Patterns

**1. Body substitute**

```text
sha256: 3f2a... length: 4821 content-class: personal -> proves sameness across two responses without storing either body
```

**2. Header record**

```text
status=200 age=118 cache-control=private, max-age=0 cf-cache-status=HIT vary=Cookie via=1.1 vendor-edge -> enough to prove shared storage
```

**3. Index line**

```text
E-014 | 2026-05-11T09:22Z | GET /account | dimension=cookie | boundary v3 | body=hash-only
```

## Pitfalls

- Pasting a response with a live session token into an issue that a vendor portal will retain forever
- Keeping raw captures in a public repository together with the disclosure report
- Losing the link between an evidence line and the probe that produced it, which makes the claim unverifiable

## Done when

- No archived evidence contains a session token, cookie or third-party personal record
- Every evidence line carries an index, a timestamp and a boundary document version

## References

- [OWASP - Content security policy and data handling](https://cheatsheetseries.owasp.org/)
- [NIST SP 800-53 - audit and accountability](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
