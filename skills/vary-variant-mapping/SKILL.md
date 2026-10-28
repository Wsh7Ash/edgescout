---
name: vary-variant-mapping
description: "Map how the vary header splits one key into variant sub-entries, since a leak or a miss behaves differently per variant rather than per path. Use when a response carries vary and later tests need to know whether two requests share a stored variant or occupy separate ones"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, vary, cache-key]
---

# Vary Variant Mapping

> Map how the vary header splits one key into variant sub-entries, since a leak or a miss behaves differently per variant rather than per path

**Use when:** a response carries vary and later tests need to know whether two requests share a stored variant or occupy separate ones

**Avoid when:** the response carries no vary directive and no other header hints at content negotiation

## Procedure

1. Record the exact vary token list from the response and note which request headers it names.
2. For each named request header, issue two requests differing only in that header and observe whether the status token separates them.
3. Include cookie and authorization in the map when the origin names them, since those variants carry identity-bound content.
4. Check whether vary is present on the first response but missing on a later one for the same path, which marks an inconsistent policy.
5. Record the variant count actually observed rather than the theoretical count implied by the header list.
6. Carry the map into the audit phase as the model of which requests can collide and which are guaranteed to be isolated.

## Signals

- Vary names a header the edge does not include in its lookup at all
- One variant is served fresh while another for the same path is served from storage
- The vary list differs between a first response and a repeat response on the same path
- Vary lists an entire header class such as cookie, implying many stored variants

## Patterns

**1. Variant map**

```text
path: /search
vary: accept-encoding, accept-language
observed variants: en, fr, default -> 3 entries, keyed by accept-language only
```

**2. Split check**

```text
two requests, same path, one header differing: same status token means one entry serves both variants, different token means the header splits the key
```

**3. Inconsistent policy**

```text
vary present on first answer and absent later: record the transition, because the missing list is where two variants can start to collide
```

## Pitfalls

- Assuming vary always appears in the stored entry when it is only sent on the first response
- Counting theoretical variants from the header list instead of the ones actually observed
- Forgetting accept-encoding, which splits variants on every path and hides the dimension you meant to study

## Done when

- A variant map records the vary list and the observed variant count per path
- Every named header has a separate observation proving keyed, unkeyed or inconsistent behaviour

## References

- [IETF RFC 9111 - Vary validation](https://www.rfc-editor.org/rfc/rfc9111)
- [MDN - Vary header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Vary)
