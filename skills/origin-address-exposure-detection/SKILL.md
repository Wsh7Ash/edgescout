---
name: origin-address-exposure-detection
description: "Notice when responses or published records reveal the address behind the edge, since an exposed origin bypasses every edge control the property relies on. Use when the assessment includes observing whether infrastructure behind the edge is discoverable from permitted sources"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, origin, recon]
---

# Origin Address Exposure Detection

> Notice when responses or published records reveal the address behind the edge, since an exposed origin bypasses every edge control the property relies on

**Use when:** the assessment includes observing whether infrastructure behind the edge is discoverable from permitted sources

**Avoid when:** origin discovery is out of scope and only edge-traversing observations are permitted

## Procedure

1. Confirm from the boundary document which sources are permitted for this observation: responses, published records, or nothing beyond the edge.
2. Read error pages, debug output, mail records and certificate records that already traverse or sit beside the permitted path.
3. Look for direct addresses in response headers, comment fields, redirects and any alternate-name entry the property publishes.
4. Record each candidate with the exact source that revealed it, and mark the source as passive or active accordingly.
5. Check whether the candidate would be reachable outside the edge only if the boundary permits such a check; otherwise leave it unverified.
6. Report exposure with the discovery source and a note on which edge controls a direct path would sidestep.

## Signals

- A response header names an internal address or a private hostname
- An error page displays an internal service address or a stack trace with one
- Published mail or certificate records point at an address the team did not intend to publish
- A debug endpoint reachable through the edge echoes upstream connection details

## Patterns

**1. Source record**

```text
candidate: 203.0.113.10
source: response header via upstream address
passive/active: passive
verified reachable: not tested (out of scope)
```

**2. Edge-control note**

```text
a direct path would skip: edge firewall rules, rate limits, geo controls and edge authentication, all listed so impact is concrete
```

**3. Allowed-source list**

```text
permitted: response headers, published records. forbidden: direct connection tests. write both before collecting anything
```

## Pitfalls

- Actively connecting to a candidate address when the boundary allows passive observation only
- Reporting a public load-balancer address as an exposed origin when it is a documented front door
- Omitting which edge controls a direct path would bypass, which leaves the impact vague

## Done when

- Each candidate has a recorded source labelled passive or active with a verification status
- The report names the specific edge controls a direct path would sidestep

## References

- [PortSwigger - SSRF as an origin discovery side effect](https://portswigger.net/web-security/ssrf)
- [OWASP - Infrastructure disclosure](https://owasp.org/www-project-web-security-testing-guide/)
