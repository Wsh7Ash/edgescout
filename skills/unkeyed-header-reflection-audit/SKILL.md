---
name: unkeyed-header-reflection-audit
description: "Look for request headers that influence the response while sitting outside the cache key, since a reflected unkeyed input is the precondition for poisoning a stored copy. Use when the key statement from fingerprinting marks a header unkeyed and the response is storable by a shared cache"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, cache-key, headers]
---

# Unkeyed Header Reflection Audit

> Look for request headers that influence the response while sitting outside the cache key, since a reflected unkeyed input is the precondition for poisoning a stored copy

**Use when:** the key statement from fingerprinting marks a header unkeyed and the response is storable by a shared cache

**Avoid when:** the header is proven keyed, or the path carries no-store so no shared copy can exist

## Procedure

1. List every header the key statement marked unkeyed and rank them by how likely they are to reach application logic.
2. For each candidate, send two requests differing only in that header and compare status, body and header set between them.
3. Prefer headers used for routing or rewrites and forwarding renames, because those are the ones applications most often trust.
4. When the body differs, capture only the differing region and record the header name that caused it, not the full body.
5. Check whether the differing response was stored, by repeating the baseline request without the injected header.
6. Record the finding as reflected-input with the pairing log, or close the header as inert with the same evidence.

## Signals

- Changing an unkeyed header changes the response body or status on an otherwise identical request
- A rewrite or routing header reaches the application even though the edge does not key on it
- The baseline request after a header-varied request returns the changed body from storage
- A reflected header value appears in a link, redirect or generated asset reference

## Patterns

**1. Pairing log**

```text
GET /path  header: none            -> 200 body-A status hit
GET /path  header: x-original-url: X -> 200 body-B status hit
baseline   header: none            -> 200 body-B status hit  <- stored copy changed
```

**2. Candidate order**

```text
start with routing and rewrite headers, then forwarded host, then forwarded proto, then any custom vendor header the origin documents as trusted
```

**3. Result label**

```text
reflected-and-stored | reflected-not-stored | inert; each label needs the pairing log line that produced it
```

## Pitfalls

- Changing two headers in one request and losing the attribution needed to describe the defect
- Concluding storage happened without running the baseline request that proves it
- Testing a header on a no-store path and reporting a poisoning risk that the policy already prevents

## Done when

- Every unkeyed header from the key statement has a pairing log entry and a result label
- Any reflected case includes a baseline request proving whether the changed body was stored

## References

- [PortSwigger - Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)
- [MDN - Forwarded header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Forwarded)
