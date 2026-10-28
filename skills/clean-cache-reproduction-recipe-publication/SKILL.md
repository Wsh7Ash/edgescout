---
name: clean-cache-reproduction-recipe-publication
description: "Publish a reproduction the vendor can run without your session state, so the report does not depend on entries only your workstation created. Use when a vendor or owner must independently reproduce an edge observation before acting on it"
pack: edgescout
version: 1.0.0
category: web-app
tags: [document, reproduction, vendor]
---

# Clean Cache Reproduction Recipe Publication

> Publish a reproduction the vendor can run without your session state, so the report does not depend on entries only your workstation created

**Use when:** a vendor or owner must independently reproduce an edge observation before acting on it

**Avoid when:** the owner already reproduced the observation themselves and only needs the evidence pack

## Procedure

1. Rewrite the internal recipe so it uses only publicly reachable requests that the boundary permits for the vendor.
2. Name the cleared state before step one: which layers must be cold and how the reader achieves that.
3. Give expected output per step, including status tokens, so the reader can tell a match from a divergence.
4. Note the environmental assumptions the recipe depends on, such as region or account state.
5. Run the published recipe once from a fresh context yourself and confirm the expected output still appears.
6. Attach the recipe to the report and mark which findings depend on it for reproduction.

## Signals

- The vendor replies that the observation does not reproduce on their side
- The recipe contains steps that only work with entries your session created
- Expected output is described in prose rather than as status values to match
- Environmental assumptions such as region are unstated

## Patterns

**1. Published recipe**

```text
precondition: empty cookie jar, edge region X
1. GET /path -> expect 200, status miss
2. GET /path -> expect 200, status hit
3. GET with <dimension> -> expect status hit, body differs from step 2
```

**2. Assumption list**

```text
assumes: account in region X, content class public, no purge in the last 60s -> listed so divergence has an explanation
```

**3. Dependency note**

```text
findings F-02 and F-05 require this recipe; findings F-01 and F-03 reproduce from the evidence block alone
```

## Pitfalls

- Publishing a recipe that silently depends on an entry created by an earlier probe
- Omitting region or account state, then reading a regional difference as a failed reproduction
- Never re-running the published version, so a later change to the property invalidates it unnoticed

## Done when

- The published recipe runs from a fresh context and produces the stated expected output
- Environmental assumptions and dependent findings are listed beside it

## References

- [PortSwigger - Writing reproducible reports](https://portswigger.net/web-security/web-cache-poisoning)
- [HackerOne - Report quality guidance](https://www.hackerone.com/)
