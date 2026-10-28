---
name: cdn-contract-inventory
description: "Establish which caching layer is contracted to do what, so an unexpected behaviour is measured against the documented configuration rather than a guess. Use when the engagement begins with several candidate edge vendors or an undocumented middle proxy sitting between client and application"
pack: edgescout
version: 1.0.0
category: web-app
tags: [cdn, inventory, architecture]
---

# CDN Contract Inventory

> Establish which caching layer is contracted to do what, so an unexpected behaviour is measured against the documented configuration rather than a guess

**Use when:** the engagement begins with several candidate edge vendors or an undocumented middle proxy sitting between client and application

**Avoid when:** a single vendor is already identified and its published caching defaults are known to the team that owns the property

## Procedure

1. Ask the owner for the current edge vendor list, zone file or DNS records showing which hostnames route through which provider.
2. Record which layer owns cache policy: origin headers, vendor dashboard rules, infrastructure-as-code, or a mix of all three.
3. Note any second tier such as an internal reverse proxy, a service mesh sidecar cache or a browser-facing service worker.
4. List the purge capabilities available to the team: per-URL, prefix, tag, or full flush, and who is allowed to trigger them.
5. Capture the documented intent per content class: static assets public, personalized responses uncached, API responses short-lived.
6. Write the inventory as a table of host, layer, policy owner and purge scope, and mark every cell you could not confirm as unknown.

## Signals

- DNS answer differs from the hostname the owner believes is being served
- Two vendors appear in the response header chain for the same asset class
- The owner describes purge behaviour that contradicts the vendor default
- A middleware cache exists that no one on the team can configure

## Patterns

**1. Layer table**

```text
host | layer | policy owner | purge scope
app.example.test | vendor-cdn | origin headers | per-url
api.example.test | vendor-cdn + internal proxy | dashboard rules | tag
assets.example.test | vendor-cdn | infrastructure-as-code | prefix
```

**2. Ownership question**

```text
For each host ask: where does a cache directive get written, who can change it, and what happens to a response that carries no directive at all. Silence on the third answer marks an implicit policy.
```

**3. Unknown cell rule**

```text
Mark any table cell you could not confirm from a document or a live response as unknown and carry it into the fingerprint phase as a question to answer.
```

## Pitfalls

- Assuming the vendor named in a marketing page is the layer actually answering the request
- Ignoring a middleware cache that never appears in vendor documentation or dashboards
- Recording purge scope from a remembered incident instead of the current configured behaviour

## Done when

- A layer table covers every in-scope host with policy owner and purge scope
- Unknown cells are listed explicitly and assigned to a fingerprint question

## References

- [MDN - HTTP caching overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [OWASP - Reverse proxy and caching misconfiguration](https://owasp.org/www-project-web-security-testing-guide/)
