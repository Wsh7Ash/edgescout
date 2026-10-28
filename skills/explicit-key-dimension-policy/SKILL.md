---
name: explicit-key-dimension-policy
description: "Write down which request dimensions belong in the cache key and which must be excluded, so key composition becomes a reviewed decision rather than an inherited default. Use when key composition was discovered by probing and no reviewed document says what the key should contain"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, cache-key, policy]
---

# Explicit Key Dimension Policy

> Write down which request dimensions belong in the cache key and which must be excluded, so key composition becomes a reviewed decision rather than an inherited default

**Use when:** key composition was discovered by probing and no reviewed document says what the key should contain

**Avoid when:** the owner already maintains a reviewed key policy that matches observed behaviour

## Procedure

1. List every dimension observed during fingerprinting and audit, marking each proven keyed, unkeyed or unknown.
2. For each dimension decide whether it must be in the key because it changes content, or excluded because it never does.
3. Write the resulting policy as a short table with one row per dimension and the reason for its placement.
4. Require that identity-bearing dimensions be present in the key wherever storage is permitted on that path.
5. Route unknown dimensions to a conservative default, either excluded from key and not stored, or keyed and documented.
6. Have the owner review and store the table beside the configuration, so a later change can be checked against it.

## Signals

- Key composition is known only to whoever last edited the vendor console
- Dimensions proven non-contributing are still splitting entries
- An unknown dimension sits in the key with no recorded reason
- Identity dimensions are absent from the key on a path that stores responses

## Patterns

**1. Policy table**

```text
dimension | placement | reason
path | in key | changes content
authorization | in key | selects identity
utm params | excluded | never changes output
x-forwarded-host | excluded and rejected | untrusted input
```

**2. Unknown default**

```text
unknown dimension -> treat as content-changing and key it, unless the owner explicitly accepts the storage cost of the alternative
```

**3. Review line**

```text
policy reviewed by <role> on <date>; every later configuration diff must explain a row it changes
```

## Pitfalls

- Writing a policy that describes current behaviour rather than what the behaviour should be
- Allowing an unknown dimension to stay in the key silently, which hides its capacity cost
- Leaving identity dimensions out of the key on a path whose responses are personalized

## Done when

- A policy table covers every dimension observed with placement and reason per row
- The owner has reviewed the table and it sits beside the configuration source

## References

- [IETF RFC 9111 - Vary and cache keys](https://www.rfc-editor.org/rfc/rfc9111)
- [OWASP - Configuration management](https://owasp.org/www-project-application-security-verification-standard/)
