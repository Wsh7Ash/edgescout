---
name: clean-state-reproduction-recipe
description: "Produce a reproduction that starts from an empty cache state every time, so a reviewer or the vendor can replay the observation without inheriting your stored entries. Use when an edge observation must be handed to a vendor or a reviewer who will replay it in a different environment"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, reproduction, evidence]
---

# Clean-State Reproduction Recipe

> Produce a reproduction that starts from an empty cache state every time, so a reviewer or the vendor can replay the observation without inheriting your stored entries

**Use when:** an edge observation must be handed to a vendor or a reviewer who will replay it in a different environment

**Avoid when:** the behaviour is deterministic and cannot depend on stored state, which a repeat request already proved

## Procedure

1. Identify every cache layer that could hold state between your requests: edge, internal proxy and browser-side storage.
2. Use a cache-busting parameter or a fresh request shape where the boundary permits it, so the lookup starts cold.
3. Open a clean client context with no cookies and no storage, so identity does not influence which entry is selected.
4. Write the exact request sequence in order, including waits, so the sequence can be replayed without interpretation.
5. Record the status token for each step so a reader can tell a cold lookup from a warm one.
6. Package the recipe with the observation it produced and note any step that a vendor might not be able to reproduce.

## Signals

- A reproduction succeeds on your machine but fails for a reviewer using a warm browser session
- The first request of a session behaves differently from every later request
- A step in the sequence has no recorded status token, leaving the state ambiguous
- The recipe relies on a stored entry from an earlier test that a purge has since removed

## Patterns

**1. Recipe block**

```text
1. open clean context, no cookies
2. GET /path?bust=1 -> expect miss
3. GET /path?bust=1 -> record status
4. GET /path -> record status and body hash
record every status token
```

**2. State declaration**

```text
declare the layers cleared before step 1: edge entry unknown, internal proxy cleared or not, browser storage cleared
```

**3. Repro note**

```text
if a step cannot be replayed outside your session, write it as an environment assumption rather than presenting it as deterministic
```

## Pitfalls

- Writing a reproduction that silently depends on entries your earlier probes created
- Omitting the clean-context step, so the reviewer's identity selects a different entry
- Presenting an environment-dependent sequence as though it were deterministic

## Done when

- A numbered recipe records every request with its status token and the cleared layers
- The recipe reproduces in a fresh context without relying on entries from earlier tests

## References

- [PortSwigger - Reproducing cache issues](https://portswigger.net/web-security/web-cache-poisoning)
- [NIST - Evidence handling guidance](https://csrc.nist.gov/publications/detail/sp/800-86/final)
