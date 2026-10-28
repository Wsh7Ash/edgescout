---
name: cross-client-leak-confirmation
description: "Confirm whether one client can receive content stored for another by alternating two sessions you own, and stop at the header evidence if bodies would diverge. Use when a path appears to serve a stored response across identities and the finding needs confirmation rather than suspicion"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, isolation, shared-cache]
---

# Cross-Client Leak Confirmation

> Confirm whether one client can receive content stored for another by alternating two sessions you own, and stop at the header evidence if bodies would diverge

**Use when:** a path appears to serve a stored response across identities and the finding needs confirmation rather than suspicion

**Avoid when:** the response marks itself private and alternating sessions already confirm isolation

## Procedure

1. Create two synthetic sessions with distinct content you own, so any mismatch is between your own records.
2. Request the same path alternately with session A, session B and then A again, recording the status token each time.
3. Compare a stable fingerprint of the response, such as a hash of a non-sensitive region, rather than archiving whole bodies.
4. Check whether the mismatch follows the session or the storage, by repeating the alternation after a purge.
5. If bodies would contain personal content beyond your own records, stop and report the header-level evidence instead.
6. Record the alternation log with the verdict: isolated, shared, or indeterminate with the reason it could not be settled.

## Signals

- Session B receives content whose fingerprint matches what session A received earlier
- The mismatch persists across several alternations rather than appearing once
- A purge changes which session receives which entry, tying the behaviour to storage rather than identity
- The origin's own logs show a single fetch while two clients received the same content

## Patterns

**1. Alternation log**

```text
A -> hash-1 hit
B -> hash-1 hit   <- mismatch, expected hash-2
A -> hash-1 hit
purge
A -> hash-2 miss
B -> hash-2 miss  <- behaviour changed after purge
```

**2. Fingerprint rule**

```text
hash a non-sensitive region such as a length or a marker string; if no such region exists, fall back to header comparison alone
```

**3. Stop condition**

```text
if confirming would require reading a third party's record, record the header evidence and mark the verdict indeterminate
```

## Pitfalls

- Continuing an alternation once bodies from another tenant would be read to settle it
- Concluding a leak from a single mismatch that a purge or expiry could explain
- Archiving full bodies as proof when a fingerprint would establish sameness

## Done when

- An alternation log records hash and status per turn for at least two full cycles
- The verdict names isolation, sharing, or indeterminate with the stop condition that applied

## References

- [OWASP - Cache-based isolation testing](https://owasp.org/www-project-web-security-testing-guide/)
- [IETF RFC 9111 - Shared cache requirements](https://www.rfc-editor.org/rfc/rfc9111)
