---
name: origin-exposure-lockdown
description: "Restrict direct access to origin infrastructure so the edge remains the only way in, restoring the value of every control the edge is expected to enforce. Use when an origin address was discovered or confirmed during detection and the owner can apply an access restriction"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, origin, network]
---

# Origin Exposure Lockdown

> Restrict direct access to origin infrastructure so the edge remains the only way in, restoring the value of every control the edge is expected to enforce

**Use when:** an origin address was discovered or confirmed during detection and the owner can apply an access restriction

**Avoid when:** the address is a documented public front door rather than an origin that should sit behind the edge

## Procedure

1. Confirm which addresses are genuinely origin endpoints rather than documented public endpoints.
2. Enumerate the legitimate callers of each origin address, including scheduled jobs, partner integrations and internal tools.
3. Apply a network restriction that admits only the edge provider's published address ranges and the enumerated callers.
4. Verify from a permitted vantage point that direct requests are refused while edge-traversing requests still succeed.
5. Record the source of the address ranges used and schedule a review, since provider ranges change over time.
6. Document the residual exposure for any caller that cannot be allow-listed, with an owner and a remediation date.

## Signals

- A direct request outside the edge reaches the application successfully
- Address ranges were copied from memory rather than a published, dated source
- A scheduled job or partner integration broke after the restriction was applied
- No review date exists for the allow-list, so drift accumulates silently

## Patterns

**1. Lockdown record**

```text
address | source of ranges | callers allow-listed | direct test | edge test
203.0.113.10 | provider published ranges 2026-05 | 4 | refused | 200
```

**2. Verification pair**

```text
one direct request from a permitted vantage point expecting refusal, one edge-traversing request expecting success, both recorded
```

**3. Residual list**

```text
caller | why it cannot be allow-listed | owner | target date -> written so nothing is quietly left open
```

## Pitfalls

- Applying a restriction that blocks a scheduled job and causes an outage the team did not ask for
- Hard-coding provider address ranges with no review date and letting them drift
- Locking down an address that was actually a public endpoint and breaking legitimate traffic

## Done when

- A lockdown record shows direct refusal and edge success for each address changed
- Residual callers that could not be allow-listed are listed with owners and dates

## References

- [OWASP - Network segmentation and access control](https://owasp.org/www-project-web-security-testing-guide/)
- [Cloudflare - Origin server protection](https://developers.cloudflare.com/fundamentals/)
