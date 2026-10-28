---
name: authorization-boundary-documentation
description: "Write down exactly which hosts, paths, header manipulations and request rates the edge-testing engagement permits before any request leaves the workstation. Use when an edge or cache assessment is about to start and the written rules of engagement name no host list, rate ceiling or permitted header set"
pack: edgescout
version: 1.0.0
category: web-app
tags: [scope, rules-of-engagement, authorization]
---

# Authorization Boundary Documentation

> Write down exactly which hosts, paths, header manipulations and request rates the edge-testing engagement permits before any request leaves the workstation

**Use when:** an edge or cache assessment is about to start and the written rules of engagement name no host list, rate ceiling or permitted header set

**Avoid when:** the program already publishes a machine-readable scope file and the signed rules of engagement list permitted verbs and header classes

## Procedure

1. Collect the signed rules of engagement, the public program page and any scope file into one place and note the document versions you used.
2. List every in-scope hostname, CDN front door, alternative port and staging alias exactly as written, without normalizing or guessing wildcards.
3. Record the permitted HTTP verbs, header manipulation classes, request-rate ceiling and the explicit ban list in one table you can quote back.
4. Confirm whether direct-to-origin requests, cache-busting query strings and authenticated sessions are allowed, since each changes the test plan.
5. Write the boundary as a short pre-flight checklist you re-read before the first request of every session, not as a note you recall from memory.
6. Save the boundary text beside the evidence you will collect so a reviewer can prove every recorded request fell inside the permitted set.

## Signals

- Rules of engagement mention hosts but are silent on header manipulation or cache-busting
- Program page says 'CDN in scope' while the origin IP is marked out of scope
- Rate limits are described in prose rather than a number you can enforce
- A previous session already recorded requests against a hostname you cannot find in writing

## Patterns

**1. Boundary record**

```text
scope:
  hosts: [app.example.test, api.example.test]
  verbs: [GET, HEAD]
  header_classes: [cache-key-probe, forward-rename]
  direct_origin: forbidden
  rate_rps: 2
  cache_bust: allowed
```

**2. Pre-flight echo**

```text
Before session start, restate: hosts, verbs, header classes, rate ceiling, and the two explicit bans. Any element you cannot quote from the document is a gap to resolve, not a permission to assume.
```

**3. Evidence binding**

```text
Store boundary.md next to evidence/*.log so each recorded request line has a document version it can be checked against during review.
```

## Pitfalls

- Reading a wildcard as permission for every subdomain when the program lists specific hosts only
- Assuming staging and production share scope because they share a hostname pattern
- Treating an old email thread as current authorization after the program changed its rules

## Done when

- A written boundary table names hosts, verbs, header classes, rate ceiling and explicit bans
- Every later evidence file carries the document version used to justify it

## References

- [PortSwigger - Web cache deception](https://portswigger.net/web-security/web-cache-deception)
- [OWASP - Testing for improper access control](https://owasp.org/www-project-web-security-testing-guide/)
