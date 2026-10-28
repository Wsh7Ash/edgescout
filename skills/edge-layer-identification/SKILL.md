---
name: edge-layer-identification
description: "Determine which caching layer actually answers a request by reading the header chain, so every later observation is attributed to the right component. Use when a hostname is in scope and the responsible vendor, proxy or internal cache has not been confirmed from a live response"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, cdn, headers]
---

# Edge Layer Identification

> Determine which caching layer actually answers a request by reading the header chain, so every later observation is attributed to the right component

**Use when:** a hostname is in scope and the responsible vendor, proxy or internal cache has not been confirmed from a live response

**Avoid when:** the owner has already supplied a documented layer diagram that matches observed response headers

## Procedure

1. Send a GET for a stable public asset and capture the complete response header set verbatim, including the order headers appear in.
2. Look for vendor signatures such as a ray identifier, an edge request id, a served-by token or a generic cache status header.
3. Record every layer named in the via and forwarded chains, since more than one cache may be answering the same request.
4. Compare a cacheable asset with a dynamic route to see which headers persist across content classes.
5. Repeat once with a cache-busting parameter to see which headers change between a miss and a hit.
6. Write the identified layers into the inventory table with the header evidence that justified each entry.

## Signals

- A ray or request id header appears only on responses that crossed a vendor edge
- The via chain names an intermediary the owner did not list in the architecture note
- Header names differ between a static asset and a dynamic route on the same host
- A cache status header changes value when only the query string changes

## Patterns

**1. Signature table**

```text
header | example value | layer implied
server | vendor-edge/2.3 | edge vendor
via | 1.1 vendor-edge | edge hop present
x-cache | hit from edge | edge stored the response
x-request-id | 8f2c... | origin correlation id
```

**2. Miss-hit pair**

```text
Same path requested twice with different cache-busting values: the header present only on the second answer marks the storing layer.
```

**3. Chain notation**

```text
client -> vendor-edge -> internal-proxy -> origin, each layer written only when a header in the response proves that hop exists
```

## Pitfalls

- Attributing storage to the vendor whose logo appears in a server header while an internal proxy holds the copy
- Reading a generic cache header as vendor proof when the origin emits the same header itself
- Fingerprinting once and assuming every content class traverses an identical chain

## Done when

- Every in-scope host has a recorded layer chain with the header evidence for each hop
- Cache status behaviour is confirmed on at least two content classes

## References

- [MDN - Via header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Via)
- [IETF RFC 9111 - HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)
