---
name: freshness-and-age-derivation
description: "Derive how long a stored response stays fresh from cache-control and age, so probe timing matches the property's real storage window instead of a guess. Use when planning repeat observations where the remaining freshness lifetime determines whether a second request reaches the origin"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, ttl, headers]
---

# Freshness and Age Derivation

> Derive how long a stored response stays fresh from cache-control and age, so probe timing matches the property's real storage window instead of a guess

**Use when:** planning repeat observations where the remaining freshness lifetime determines whether a second request reaches the origin

**Avoid when:** the response carries no-store or no-cache and therefore never becomes fresh in any shared cache

## Procedure

1. Read cache-control from the response and record each directive that affects storage: max-age, s-maxage, no-store, no-cache, private, must-revalidate.
2. Read the age header to learn how long the stored copy has already been in the cache before your request reached it.
3. Compute remaining freshness as max-age minus age, using s-maxage where a shared cache honours it over max-age.
4. Check whether a later response from the same path reports a smaller age, which indicates revalidation or a fresh store rather than expiry.
5. Record the derived window beside the path so probe spacing can sit comfortably inside it.
6. Note any path where the origin sets one lifetime and the observed window is longer, since a second policy layer is overriding the header.

## Signals

- Observed storage outlives the longest directive the origin ever sent
- The age value grows across requests and then resets without a purge
- s-maxage and max-age differ, and the shared cache appears to honour the larger one
- A no-store response still returns an age header from an upstream layer

## Patterns

**1. Window arithmetic**

```text
remaining = max_age - age_seconds; probe twice inside remaining, then once after it to observe revalidation behaviour
```

**2. Directive table**

```text
max-age=60 s-maxage=300 -> shared cache may hold 300s, browser holds 60s
no-store -> no store anywhere, age header should stay 0
private -> shared cache must not store, single client may
```

**3. Override check**

```text
header says max-age=60 but observed window is 300s: write 'policy layer present' and continue fingerprinting the layer that added it
```

## Pitfalls

- Spacing probes by a remembered default instead of the lifetime this response actually declares
- Treating an age header on a no-store response as proof that storage occurred
- Computing the window from max-age while the shared cache honours a different directive

## Done when

- A freshness window is recorded per tested path with the directives that produced it
- Probe spacing sits inside the derived window and is repeated once outside it

## References

- [IETF RFC 9111 - Calculating freshness lifetime](https://www.rfc-editor.org/rfc/rfc9111)
- [MDN - Cache-Control max-age](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
