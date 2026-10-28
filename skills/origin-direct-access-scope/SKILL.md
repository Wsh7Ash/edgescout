---
name: origin-direct-access-scope
description: "Determine whether contacting the origin outside the edge is permitted, because this single decision changes both the test plan and the class of finding you may produce. Use when an origin address may be discoverable from DNS history, certificates or headers and the rules of engagement are silent on direct contact"
pack: edgescout
version: 1.0.0
category: web-app
tags: [origin, scope, architecture]
---

# Origin Direct Access Scope

> Determine whether contacting the origin outside the edge is permitted, because this single decision changes both the test plan and the class of finding you may produce

**Use when:** an origin address may be discoverable from DNS history, certificates or headers and the rules of engagement are silent on direct contact

**Avoid when:** the program states plainly that origin addresses are out of scope or that all traffic must pass through the edge

## Procedure

1. Search the rules of engagement for the exact terms origin, direct, bypass and IP, and quote the surrounding sentences verbatim in your notes.
2. When the document is silent, ask the program a direct yes-or-no question about origin contact and wait for the answer before proceeding.
3. If origin contact is out of scope, restrict discovery to passive observations already visible in responses that traverse the edge.
4. When permitted, plan a low-rate request set against the origin that mirrors only the synthetic content used elsewhere in the engagement.
5. Record which findings depend on origin access so a reader can distinguish an edge defect from an origin exposure.
6. Re-confirm the decision at any change of engagement, since scope updates often reverse this one item without changing host lists.

## Signals

- Rules of engagement list a hostname but never mention the address behind it
- Certificate transparency or DNS history already reveals candidate origin addresses
- Responses differ depending on whether the request arrived through the edge
- The program has no written answer to a direct origin-contact question

## Patterns

**1. Decision record**

```text
origin_direct: unknown | permitted | forbidden
source: <document section or program reply>
date: <ISO date>
consequence: passive only | low-rate direct tests allowed
```

**2. Passive fallback**

```text
If origin contact is forbidden, derive evidence only from edge-traversing responses: header chains, error page fingerprints, and routing differences observed from the permitted path.
```

**3. Finding label**

```text
Tag every finding as edge-observed or origin-observed so a reader never infers a bypass result from a test the boundary forbade.
```

## Pitfalls

- Probing an origin address that a program considers private infrastructure and turning a finding into a scope breach
- Concluding that an origin is unreachable because a firewall rejected the request you were not cleared to send
- Reporting an origin exposure as an edge defect when the two layers were never separated in evidence

## Done when

- Origin contact is recorded as permitted or forbidden with a quoted source
- Every finding produced later carries an edge-observed or origin-observed label

## References

- [PortSwigger - Server-side request forgery](https://portswigger.net/web-security/ssrf)
- [OWASP - Edge and origin security](https://owasp.org/www-project-web-security-testing-guide/)
