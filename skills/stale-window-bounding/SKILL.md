---
name: stale-window-bounding
description: "Cap how long a stored response may be served after its revocation point, so a deleted document or a closed account cannot be replayed for hours. Use when the audit measured a worst-case serving window that exceeds the property's revocation expectation"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, ttl, policy]
---

# Stale Window Bounding

> Cap how long a stored response may be served after its revocation point, so a deleted document or a closed account cannot be replayed for hours

**Use when:** the audit measured a worst-case serving window that exceeds the property's revocation expectation

**Avoid when:** the measured window already sits inside the stated revocation expectation on every tested path

## Procedure

1. Record the measured worst-case window and the revocation expectation it violates, both with their sources.
2. Reduce the stale allowances on the affected class to a value that fits inside the expectation with margin.
3. Apply must-revalidate where a stored entry may not be reused once stale without a successful revalidation.
4. Re-measure the window after the change by repeating the directive and freshness calculation on a live response.
5. Check that reducing the window did not break the availability behaviour the allowance originally protected.
6. Record the before and after windows with the configuration change that produced the difference.

## Signals

- A stale allowance outlives the property's stated revocation expectation
- Reducing the allowance caused availability problems that were not anticipated
- The change was applied at one layer while a second layer still permits the longer window
- The after window was never re-measured, so the fix rests on a calculation only

## Patterns

**1. Before and after**

```text
before: max-age=3600 + swr=86400 -> 90000s
after: max-age=300 + swr=60 + must-revalidate -> 360s
expectation: 900s -> now inside the bound
```

**2. Layer sweep**

```text
re-read directives at every layer that attaches them; one layer accepting the bound while another does not leaves the defect in place
```

**3. Availability check**

```text
repeat the request during a simulated origin error if permitted, to confirm the reduced allowance did not remove the protection it existed for
```

## Pitfalls

- Changing only one layer's directives and leaving the other able to extend the window
- Cutting an allowance without checking what availability behaviour depended on it
- Trusting the arithmetic without re-reading a live response after the change

## Done when

- Before and after windows are recorded with the configuration change that produced them
- The after window fits inside the stated expectation on a live response, not only on paper

## References

- [IETF RFC 5861 - Stale response directives](https://www.rfc-editor.org/rfc/rfc5861)
- [MDN - Cache-Control directives reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
