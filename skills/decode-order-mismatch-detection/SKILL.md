---
name: decode-order-mismatch-detection
description: "Detect when the edge and the origin decode a request differently, since a decoding gap lets one interpretation reach the cache and a different one reach the application. Use when the key statement shows encoding affects lookup and the origin may decode input on a different schedule than the edge"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, encoding, cache-key]
---

# Decode Order Mismatch Detection

> Detect when the edge and the origin decode a request differently, since a decoding gap lets one interpretation reach the cache and a different one reach the application

**Use when:** the key statement shows encoding affects lookup and the origin may decode input on a different schedule than the edge

**Avoid when:** both layers are proven to produce identical normalized paths and parameters for every variant tested

## Procedure

1. Build a small variant set covering single encoding, double encoding, mixed case escapes and an overlong separator.
2. Request each variant and record status, location and cache status token without adding any other variation.
3. Compare the edge's view of the normalized path with the origin's view, using the application's own routing response as the origin side.
4. Look for a case where two variants land on one stored entry while the origin treats them as different routes.
5. Check whether a rejected variant's error response is stored and later served for an accepted variant.
6. Record each mismatch with the variant pair, the stored entry they shared and how the origin treated each.

## Signals

- Two encodings of one path share a stored entry while the origin routes them differently
- An error for one variant is stored and later returned for a different variant
- A decoded path reaches the application with a form the edge never evaluated
- Trailing-separator or dot-segment variants normalize differently at each layer

## Patterns

**1. Variant pair**

```text
variant A: /path%2fsub -> stored entry E1, origin route: /path/sub
variant B: /path/sub    -> stored entry E1, origin route: /path/sub  <- same entry, confirm intentionally
```

**2. Decode ladder**

```text
note decode count at each layer: edge once, application twice, or the reverse; an unequal ladder is where interpretations diverge
```

**3. Error reuse line**

```text
stored 404 for variant A later returned for variant B: record both spellings and the status token on each response
```

## Pitfalls

- Testing only fully encoded variants and missing the mixed or double-encoded case where layers disagree
- Concluding a mismatch without asking the origin how it routed each variant
- Reporting a decode difference that has no effect because no entry is stored for either variant

## Done when

- A variant table records status, location and cache token for every encoding tested
- Any shared entry names both spellings and states how the origin routed each

## References

- [IETF RFC 3986 - Percent-encoding normalization](https://www.rfc-editor.org/rfc/rfc3986)
- [PortSwigger - Path confusion](https://portswigger.net/web-security/request-smuggling)
