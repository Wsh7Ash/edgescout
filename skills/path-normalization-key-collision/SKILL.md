---
name: path-normalization-key-collision
description: "Find path spellings that normalize to one stored entry, so two logically different resources are shown to share a cache key they were never meant to share. Use when the edge and the origin may disagree about path decoding, case or default documents on an in-scope host"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, cache-key, paths]
---

# Path Normalization Key Collision

> Find path spellings that normalize to one stored entry, so two logically different resources are shown to share a cache key they were never meant to share

**Use when:** the edge and the origin may disagree about path decoding, case or default documents on an in-scope host

**Avoid when:** the origin is proven to normalize identically to the edge and both layers return the same status for every variant tested

## Procedure

1. Build a variant list for one representative path: default document, trailing separator, encoded separator, dot segment and upper case.
2. Request each variant without any cache-busting parameter and record status, location header and cache status token.
3. Compare the edge answer with the origin's own view by checking whether the application treats two variants as one route.
4. Look for a case where a 404 or a redirect for one variant is served in place of the correct resource for another.
5. Repeat the collision check after the storage window expires, since an expired entry may behave differently from a fresh one.
6. Record each collision with the exact spelling pair and the shared status both spellings received.

## Signals

- Two spellings of one path return an identical stored response with an identical status token
- An encoded separator variant returns the default document or a redirect meant for another route
- Case variants share one stored entry on a path where the origin is case sensitive
- A trailing separator triggers a redirect that is then stored and replayed for the canonical path

## Patterns

**1. Variant set**

```text
/path, /path/, /path/index.html, /path%2f, /./path, /PATH  -> record status, location and cache token for each
```

**2. Collision line**

```text
spelling A: /account/  -> 200, hit
spelling B: /account   -> 200, hit, same body hash -> one entry serves both spellings
```

**3. Redirect capture**

```text
if a redirect for a variant is stored, note the target: replaying it for the canonical path turns a cosmetic issue into a routing defect
```

## Pitfalls

- Testing only the canonical spelling and never the separator, encoding and case variants
- Treating a redirect difference as cosmetic when the redirect itself is what gets stored
- Ignoring that a collision is only reportable when both spellings are in scope for the assessment

## Done when

- Each tested path has a variant table with status, location and cache token per spelling
- Any collision records both spellings and the shared response they received

## References

- [IETF RFC 3986 - Path component syntax](https://www.rfc-editor.org/rfc/rfc3986)
- [PortSwigger - Web cache deception](https://portswigger.net/web-security/web-cache-deception)
