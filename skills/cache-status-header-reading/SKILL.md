---
name: cache-status-header-reading
description: "Read each vendor's cache status vocabulary correctly and map it onto the shared hit and miss states, so a test result is never misread because of naming differences. Use when responses carry a cache status header from an unfamiliar vendor or the same word means different things across two layers"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, headers, cache-status]
---

# Cache Status Header Reading

> Read each vendor's cache status vocabulary correctly and map it onto the shared hit and miss states, so a test result is never misread because of naming differences

**Use when:** responses carry a cache status header from an unfamiliar vendor or the same word means different things across two layers

**Avoid when:** no status header is present and behaviour must be derived from timing and repeat-request comparison instead

## Procedure

1. Capture the vendor's status header verbatim on a first request, a second identical request and a request after a purge, if a purge is permitted.
2. Map each observed value onto the shared vocabulary of hit, miss, refresh, expired and bypass before drawing any conclusion.
3. Note compound values where a layer reports upstream and local states in one token, since only one of them describes storage.
4. Check whether the header is present on error responses as well, because cached errors change availability behaviour.
5. Record which content classes produce which status values, since policy often differs between static and dynamic routes.
6. Keep the mapping table with your evidence so a reader who knows another vendor can follow the result.

## Signals

- The same vendor token appears with a qualifier that names a second layer
- A status value flips between two tokens without any change to the request
- Error responses carry a status token identical to successful cached responses
- One content class never reports a status header at all

## Patterns

**1. State map**

```text
vendor token -> shared state
hit, fresh, served-from-edge -> hit
miss, not-in-cache, refresh -> miss
expired, stale, revalidated -> expired
bypass, no-store, uncacheable -> bypass
```

**2. Compound value**

```text
tcp_hit/200 or HIT, HIT means the outer layer stored it; write the layer next to the token instead of collapsing both into 'cached'.
```

**3. Flip test**

```text
two identical requests, no intervening change: if the token flips, an independent event such as a purge or expiry happened and must be noted
```

## Pitfalls

- Reading a miss token as evidence the response was never stored by an upstream layer
- Comparing tokens from two vendors as if their vocabularies were defined by the same specification
- Ignoring a missing status header, which usually means the layer in front does not expose its state

## Done when

- A token mapping table exists for every status header observed in scope
- Hit, miss and bypass states are confirmed by repeat requests rather than assumed from naming

## References

- [IETF RFC 9111 - Section 4 cache validation](https://www.rfc-editor.org/rfc/rfc9111)
- [MDN - Age header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Age)
