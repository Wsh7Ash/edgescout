---
name: secondary-layer-detection
description: "Detect caching layers below the vendor edge, such as an internal proxy or service worker, because a defect in the lower layer will never show up in vendor status headers. Use when a behaviour difference exists between two clients that both traverse the same vendor edge"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, architecture, layers]
---

# Secondary Layer Detection

> Detect caching layers below the vendor edge, such as an internal proxy or service worker, because a defect in the lower layer will never show up in vendor status headers

**Use when:** a behaviour difference exists between two clients that both traverse the same vendor edge

**Avoid when:** the architecture note confirms there is exactly one caching layer between client and origin

## Procedure

1. Compare responses from two different client contexts that share the same edge, noting differences the vendor status token cannot explain.
2. Inspect the response for directives that only a downstream layer would honour, such as proxy-revalidate or a stale directive.
3. Check whether conditional requests are answered by the edge or passed through, since revalidation at a lower layer leaves a distinct header pattern.
4. Look for storage hints in service-worker or application-cache behaviour on the client side of the property.
5. Ask the owner about middleware caches, read-through caches and API gateways that store responses in front of the application.
6. Record each discovered layer in the inventory with the observation that revealed it.

## Signals

- Two clients behind the same edge receive different bodies for the same key
- A response changes only after a browser reload or a service-worker update
- The origin logs a request that the edge status header says was served from cache
- An internal proxy appears in a forwarded chain on error responses only

## Patterns

**1. Layer question list**

```text
Is there a reverse proxy with caching? a gateway cache? a read-through cache? a browser service worker? an application-level memoization of responses? Record each answer with a source.
```

**2. Evidence pair**

```text
client A hit/body-1 and client B hit/body-2 on the same key: the differentiator must be a layer below the edge or an unkeyed dimension
```

**3. Revalidation trace**

```text
conditional request answered with 304 at the edge versus forwarded to origin: the header set differs and identifies which layer validated
```

## Pitfalls

- Stopping the fingerprint once the vendor edge is identified while an internal cache holds the interesting copy
- Blaming the edge for a difference produced by a service worker running on the client
- Assuming an internal cache was disabled because it does not appear in vendor documentation

## Done when

- Every identified caching layer appears in the inventory with a revealing observation
- Behaviour that vendor status headers cannot explain is attributed to a named layer

## References

- [MDN - Service worker overview](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [OWASP - Reverse proxy testing](https://owasp.org/www-project-web-security-testing-guide/)
