---
name: redirect-chain-storage-behavior
description: "Trace how each hop of a redirect chain is stored, because a cached intermediate hop can trap clients in a loop or send them to a target that has since changed. Use when an in-scope path answers with redirects and any hop may be subject to shared storage"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, redirects, cache-key]
---

# Redirect Chain Storage Behavior

> Trace how each hop of a redirect chain is stored, because a cached intermediate hop can trap clients in a loop or send them to a target that has since changed

**Use when:** an in-scope path answers with redirects and any hop may be subject to shared storage

**Avoid when:** the path returns a single permanent redirect that the owner confirms is immutable

## Procedure

1. Follow the chain hop by hop and record status, location header and cache status token for each hop separately.
2. Check which hops are stored and for how long, using the freshness directives each hop carries.
3. Look for a hop whose stored location differs from what the origin currently returns for that same path.
4. Test whether a purge of the first hop clears the later hops or leaves intermediate entries in place.
5. Check for a loop that only appears when a stored hop is combined with a client-side redirect rule.
6. Record the chain as a table of hop, status, location, stored, lifetime, with the anomaly in its own row.

## Signals

- An intermediate hop is stored while the final target is not
- A stored location points at a target the origin has since changed
- Purging the first hop leaves a later hop still reported as stored
- The chain behaves differently when replayed from a clean context than from a warm one

## Patterns

**1. Hop table**

```text
hop 1: 301 location /a hit lifetime 86400
hop 2: 302 location /b miss lifetime 0
hop 3: 200 hit lifetime 3600
```

**2. Target drift**

```text
stored location on hop 1 vs current origin location: if they differ, record the old target and the moment it stopped being correct
```

**3. Purge sweep**

```text
purge hop 1, then re-request each later hop: entries that survive are the ones the purge scope did not reach
```

## Pitfalls

- Reporting the chain as a whole when only one specific hop is stored or wrong
- Following redirects with a tool that caches locally and confusing that with edge storage
- Missing a loop that requires a clean context to appear, because a warm session follows different hops

## Done when

- A hop table records status, location, stored state and lifetime for every hop
- Target drift and purge sweep results are recorded as separate rows with evidence

## References

- [IETF RFC 9110 - Redirect status codes](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN - Location header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Location)
