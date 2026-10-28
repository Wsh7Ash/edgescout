---
name: conditional-request-behavior-audit
description: "Check how validators behave at the edge, since a mismatched etag or not-modified handling can serve stale state or mask an update that already happened at the origin. Use when responses carry validators such as etag or last-modified and the edge participates in revalidation"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, validators, revalidation]
---

# Conditional Request Behavior Audit

> Check how validators behave at the edge, since a mismatched etag or not-modified handling can serve stale state or mask an update that already happened at the origin

**Use when:** responses carry validators such as etag or last-modified and the edge participates in revalidation

**Avoid when:** the path uses no validators and revalidation never occurs for any tested request

## Procedure

1. Capture the etag and last-modified values from an initial response and record whether the edge reported it as stored.
2. Send a conditional request with the captured validator and record status, headers and cache status token.
3. Modify content through the application's own supported path if permitted, then repeat the conditional request.
4. Check whether the edge revalidated against the origin or answered from its stored copy without contacting it.
5. Verify that a changed etag at the origin produces a fresh answer at the edge rather than a not-modified built from stale state.
6. Record each conditional exchange with the validator used, the status and which layer answered it.

## Signals

- A conditional request returns not-modified while the origin's current content hash differs
- The etag reported by the edge never changes after an update made through the application
- A conditional request is answered from storage without a corresponding origin fetch in logs
- Weak and strong validators are mixed in a way that lets a changed body keep an old validator

## Patterns

**1. Exchange line**

```text
if-none-match: W/"abc" -> 304, status hit, origin fetch: none -> edge answered alone
after update: if-none-match: W/"abc" -> 200, status miss, new etag -> revalidated
```

**2. Validator compare**

```text
record origin etag and edge-reported etag per observation; a persistent mismatch marks stale revalidation state
```

**3. Layer attribution**

```text
304 with no origin fetch means the edge held the validator; a 304 accompanied by an origin fetch means the origin confirmed it
```

## Pitfalls

- Reading a 304 as proof the content is current when only the edge's stored copy was consulted
- Comparing validators across representations that were never meant to be the same resource
- Skipping the update step, which is the only way to see whether revalidation actually reaches the origin

## Done when

- Each conditional exchange records validator, status, cache token and origin involvement
- At least one exchange is repeated after a content update to confirm revalidation behaviour

## References

- [IETF RFC 9110 - Conditional requests](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN - ETag header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag)
