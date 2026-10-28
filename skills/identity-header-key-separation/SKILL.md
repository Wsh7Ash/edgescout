---
name: identity-header-key-separation
description: "Verify that identity-bearing headers separate stored entries, since a key that ignores identity is the shortest path from one account's content to another's. Use when content selection depends on identity headers such as cookie or authorization and storage is permitted on the path"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, authentication, cache-key]
---

# Identity Header Key Separation

> Verify that identity-bearing headers separate stored entries, since a key that ignores identity is the shortest path from one account's content to another's

**Use when:** content selection depends on identity headers such as cookie or authorization and storage is permitted on the path

**Avoid when:** the response is marked no-store, in which case no shared entry can exist for any identity

## Procedure

1. Identify which header the origin actually uses to select content, by inspecting its own responses rather than guessing.
2. Build two synthetic sessions you own that produce visibly different content on the same path.
3. Request the path with each session and record status token, cache token and a fingerprint of a non-sensitive region.
4. Request the path with no identity header at all to see whether an unauthenticated answer occupies the same entry.
5. Check whether the identity header appears in the key statement, and record the verdict if it does not.
6. Report separation as proven, broken or indeterminate with the alternation evidence for each case.

## Signals

- The key statement lists no identity header while the origin selects content by one
- An unauthenticated request receives content that belongs to a session
- Two sessions receive the same fingerprint on a path meant to be per-account
- Removing the identity header changes nothing about which stored entry answers

## Patterns

**1. Separation line**

```text
session A -> hash-1, hit
session B -> hash-2, hit
no identity -> hash-1, hit  <- unauthenticated share with A
```

**2. Identity discovery**

```text
ask the origin: send two requests differing only in the identity header and see whether content changes; that header is the one the key must include
```

**3. Verdict labels**

```text
proven (all three requests separate correctly) | broken (any sharing observed) | indeterminate (bodies could not be compared)
```

## Pitfalls

- Assuming the key includes a header that the origin uses without ever proving it
- Concluding separation from a single pair when a cold store can produce the same appearance
- Continuing an alternation that would require reading another tenant's content to settle

## Done when

- Three-way evidence covers two sessions plus an unauthenticated request with fingerprints recorded
- The verdict is labelled proven, broken or indeterminate with the evidence attached

## References

- [OWASP - Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [IETF RFC 9111 - Shared cache key requirements](https://www.rfc-editor.org/rfc/rfc9111)
