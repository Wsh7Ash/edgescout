---
name: stale-window-overflow-audit
description: "Measure how long content can be served past its revocation point through stale allowances, since a revoked document or a deleted account may still be replayed for hours. Use when responses carry stale-while-revalidate, stale-if-error or must-revalidate in combination with a meaningful freshness lifetime"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, ttl, freshness]
---

# Stale Window Overflow Audit

> Measure how long content can be served past its revocation point through stale allowances, since a revoked document or a deleted account may still be replayed for hours

**Use when:** responses carry stale-while-revalidate, stale-if-error or must-revalidate in combination with a meaningful freshness lifetime

**Avoid when:** the response uses no stale allowances and must-revalidate is enforced on every tested path

## Procedure

1. Record every stale-related directive on the response with its numeric value where the directive takes one.
2. Compute the worst-case serving window as freshness lifetime plus the largest stale allowance the policy permits.
3. Compare that window with the property's own revocation expectations, such as how fast a document removal must take effect.
4. Check whether an error at the origin extends serving further under a stale-if-error allowance.
5. Verify what happens to a stored entry when the application explicitly purges it, since a purge should override any allowance.
6. Report the worst-case window with the directives that produce it and the revocation expectation it violates.

## Signals

- A stale allowance is large enough to outlive a document revocation or an account deletion
- An error response at the origin triggers extended serving of an older copy
- A purge does not take effect immediately on a path with a stale allowance
- must-revalidate is absent while a long stale allowance is configured

## Patterns

**1. Worst-case line**

```text
max-age=3600 + stale-while-revalidate=86400 -> up to 90000s of continued serving after the stated lifetime
```

**2. Revocation compare**

```text
property expectation: revocation within 15 minutes; observed worst case: 25 hours -> gap written with both numbers
```

**3. Purge override test**

```text
purge the path with permission, then re-request: an immediate miss proves the purge wins, a stale hit proves the allowance wins
```

## Pitfalls

- Adding directives incorrectly and overstating or understating the serving window
- Reporting a theoretical window without checking whether a purge overrides it in practice
- Ignoring the error path, which is often the case where the longest serving window appears

## Done when

- A worst-case window is computed per tested path with the directives shown
- The purge override behaviour is confirmed by an observed request after a purge

## References

- [IETF RFC 5861 - HTTP cache-control extensions for stale responses](https://www.rfc-editor.org/rfc/rfc5861)
- [MDN - Stale-while-revalidate](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
