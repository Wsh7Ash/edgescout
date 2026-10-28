---
name: overbroad-match-rule-review
description: "Identify cache rules whose match scope covers dynamic or personalized paths, since a single wildcard is often the whole cause of unintended storage. Use when the owner describes rules in wildcard form or observed storage covers more paths than the team intended"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, configuration, policy]
---

# Overbroad Match Rule Review

> Identify cache rules whose match scope covers dynamic or personalized paths, since a single wildcard is often the whole cause of unintended storage

**Use when:** the owner describes rules in wildcard form or observed storage covers more paths than the team intended

**Avoid when:** rules are expressed per content class and each tested path is matched by an explicit rule rather than a wildcard

## Procedure

1. Ask for the rule set in effect, or infer it from behaviour, and write each rule's match expression verbatim.
2. Map every tested path to the rule that matched it, starting with the broadest wildcard that applies.
3. Identify dynamic routes, such as account or API paths, that fall under a broad asset rule.
4. Check whether a negation or bypass list exists for the dynamic routes and whether it is evaluated before the wildcard.
5. Verify that a path intended to be excluded actually reports no storage on a repeat request.
6. Report each overbroad match with the rule text, the paths it captures and the specific paths that should be excluded.

## Signals

- A single wildcard rule appears to govern asset and application routes alike
- An account or API path reports storage despite the team believing it excluded
- A bypass list exists but is evaluated after the wildcard that already matched
- Excluding a path requires editing a rule the team does not own

## Patterns

**1. Rule map**

```text
rule: /* -> captures: /assets/*, /account/*, /api/*
rule: !/api/* -> evaluated after, never reached for these paths
```

**2. Path-to-rule line**

```text
/account/settings | matched by /* at priority 1 | expected: excluded | observed: stored -> finding
```

**3. Order note**

```text
record the evaluation order of rules, because a correct exclusion evaluated after a broader match has no effect at all
```

## Pitfalls

- Reporting the wildcard as the defect when the real defect is the order the rules are evaluated in
- Assuming a path is excluded because a negation exists rather than because a request proved it
- Testing only one dynamic route when the wildcard captures a whole class of them

## Done when

- Every tested path maps to the rule that matched it with the rule text recorded
- Excluded paths are proven excluded by a repeat request, not by the existence of a negation

## References

- [OWASP - Access control and cache configuration](https://owasp.org/www-project-web-security-testing-guide/)
- [Cloudflare - Cache rule evaluation order](https://developers.cloudflare.com/cache/)
