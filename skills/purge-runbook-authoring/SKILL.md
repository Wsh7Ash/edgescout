---
name: purge-runbook-authoring
description: "Write the purge procedure for each content class, including who may trigger it and how fast it must take effect, so content removal is a rehearsed step rather than an improvisation. Use when content removal depends on purge and no written procedure exists for when and how to clear entries"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, purge, operations]
---

# Purge Runbook Authoring

> Write the purge procedure for each content class, including who may trigger it and how fast it must take effect, so content removal is a rehearsed step rather than an improvisation

**Use when:** content removal depends on purge and no written procedure exists for when and how to clear entries

**Avoid when:** short lifetimes make purge unnecessary and the owner confirms removal never relies on it

## Procedure

1. List each content class and the purge type that reaches all of its entries, including keyed variants.
2. Record the role authorized to trigger each purge type and the escalation path when that role is unavailable.
3. State the expected propagation time per purge type, measured from an earlier test rather than assumed.
4. Describe the verification step: which request to send afterwards and what status token proves the purge landed.
5. Cover the failure path: what to do when verification still shows a stored copy after the expected delay.
6. Store the runbook with the operations documentation and rehearse it once against a synthetic path.

## Signals

- No written procedure exists for removing a specific class of content
- Only one person knows how to trigger the purge type a class requires
- Propagation time is stated as a guess rather than a measurement
- There is no verification step to prove a purge actually cleared the entry

## Patterns

**1. Runbook entry**

```text
class: article | purge: tag | role: release-engineer | expected: 60s | verify: GET with bust -> expect miss
```

**2. Verification line**

```text
after purge, request the canonical path, one keyed variant and one expired entry; all three must report a miss
```

**3. Escalation**

```text
if any of the three still reports a hit after the expected delay, escalate to <role> and fall back to <fallback purge type>
```

## Pitfalls

- Writing a runbook that covers only the canonical URL while variants survive it
- Naming a role that no current team member actually holds
- Skipping rehearsal, so the first real use of the runbook is during an incident

## Done when

- Every content class has a runbook entry with purge type, role, expected delay and verification
- The procedure has been rehearsed once against a synthetic path with the result recorded

## References

- [IETF RFC 9111 - Invalidating stored responses](https://www.rfc-editor.org/rfc/rfc9111)
- [OWASP - Incident response guidance](https://owasp.org/www-project-application-security-verification-standard/)
