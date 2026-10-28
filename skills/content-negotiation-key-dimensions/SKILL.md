---
name: content-negotiation-key-dimensions
description: "Audit how accept, accept-encoding and accept-language participate in the key, since negotiation mismatches serve one client's representation to another. Use when the response varies on a negotiation header or the application renders different bodies per client preference"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, content-negotiation, vary]
---

# Content Negotiation Key Dimensions

> Audit how accept, accept-encoding and accept-language participate in the key, since negotiation mismatches serve one client's representation to another

**Use when:** the response varies on a negotiation header or the application renders different bodies per client preference

**Avoid when:** the path returns one fixed representation and the vary list is empty on every observed response

## Procedure

1. Record the vary list the response carries and identify which negotiation headers it names.
2. For each named header, request two clearly different preferences and confirm the status token separates the two variants.
3. Test a preference the vary list omits, because an omission there is where one variant can be served to another client.
4. Check whether the edge honours the preference itself, such as serving a compressed variant without asking the origin.
5. Verify that a stored variant carries its own vary list forward so later readers of that copy see the same constraint.
6. Document the negotiation matrix: header, values tested, keyed or not, body actually returned.

## Signals

- The vary list omits a negotiation header that clearly changes the rendered body
- A compressed variant is served to a client that did not request it
- The stored copy's vary list differs from the vary list on the first response
- One variant receives a long freshness lifetime while another is never stored

## Patterns

**1. Negotiation matrix**

```text
header | values | keyed | body returned
accept-encoding | gzip, identity | yes | matches request
accept-language | en, fr | no | always en  <- omission
accept | json, html | yes | matches request
```

**2. Stored-vary check**

```text
first response: vary: accept-encoding
stored response: vary absent -> the stored entry lost its constraint, record the transition
```

**3. Honor test**

```text
request an encoding the origin does not support and note whether the edge answers from storage anyway instead of passing the request through
```

## Pitfalls

- Assuming the vary list the origin sends is the list the edge actually applies
- Testing negotiation only with well-formed values and missing the absent-header case
- Forgetting that accept-encoding changes every variant count and distorts the rest of the matrix

## Done when

- A negotiation matrix records each header, the values tested and the keyed verdict
- The stored copy's vary list is compared with the first response's list for every tested path

## References

- [IETF RFC 9110 - Content negotiation](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN - Accept-Encoding header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Encoding)
