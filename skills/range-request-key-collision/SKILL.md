---
name: range-request-key-collision
description: "Check whether partial-content requests share a key with full requests, because a range answer stored under one key can be replayed as another client's whole resource. Use when the property serves resources that clients request with range headers, such as downloads or media"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, range, cache-key]
---

# Range Request Key Collision

> Check whether partial-content requests share a key with full requests, because a range answer stored under one key can be replayed as another client's whole resource

**Use when:** the property serves resources that clients request with range headers, such as downloads or media

**Avoid when:** the origin returns the complete resource for every request regardless of the range header

## Procedure

1. Request the resource normally and record the full answer's status, cache token and content length.
2. Request the same path with a range header covering a small span and record status, content range and cache token.
3. Repeat the full request after the ranged one to see whether a partial answer is returned where the whole resource is expected.
4. Check whether the range header participates in the key, using the pairing evidence from the two requests.
5. Test a second range span to see whether different spans share one entry or create separate entries.
6. Record the collision as observed, not observed, or indeterminate, with the request pair that justifies the label.

## Signals

- A request with no range header returns a partial answer after a ranged request was made
- The cache status token is identical for a full request and a ranged request on the same path
- Different spans appear to share one stored entry
- A content range header is present on an answer to a request that sent no range

## Patterns

**1. Pair log**

```text
GET /file            -> 200, length 100000, hit
GET /file Range 0-99  -> 206, content-range 0-99, hit
GET /file            -> 206, content-range 0-99 -> collision observed
```

**2. Span compare**

```text
range 0-99 and range 100-199: same status token means one entry for both spans, different token means spans are keyed separately
```

**3. Verdict labels**

```text
collision observed | no collision | indeterminate, each written with the pair line rather than a narrative claim
```

## Pitfalls

- Reporting a collision from a single pair without the follow-up full request that reveals replay
- Testing one span only, which cannot distinguish sharing from per-span storage
- Forgetting that some servers ignore range requests entirely, making the whole check meaningless for that path

## Done when

- A pair log records full, ranged and post-ranged requests with status, length and cache token
- A span comparison shows whether spans share or split the stored entry

## References

- [IETF RFC 9110 - Range requests](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN - Range header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Range)
