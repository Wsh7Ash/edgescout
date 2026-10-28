---
name: personalized-response-private-default
description: "Make privacy the default for responses that carry identity-bound content, so a missing header cannot quietly turn into shared storage. Use when any content class varies by session, account or tenant and the current default permits shared storage"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, privacy, policy]
---

# Personalized Response Private Default

> Make privacy the default for responses that carry identity-bound content, so a missing header cannot quietly turn into shared storage

**Use when:** any content class varies by session, account or tenant and the current default permits shared storage

**Avoid when:** the class is already marked private or no-store by a rule that applies to the whole class

## Procedure

1. Identify every content class whose body depends on identity, using the class ladder recorded during scope.
2. Set the default for those classes to private and no-store at the layer that attaches directives.
3. Confirm the edge honours the default rather than overriding it with a broader rule.
4. Test a new path added after the change, since a default is only proven by a path nobody hand-configured.
5. Add a regression check to the deployment pipeline that fails when a personalized route omits the directives.
6. Record the classes covered and the path used to prove the default, so coverage can be audited later.

## Signals

- A newly added personalized route ships without private or no-store
- The edge overrides the origin default for a class the team believes is protected
- A pipeline check does not exist, so a header omission ships unnoticed
- Coverage lists paths individually instead of covering a content class

## Patterns

**1. Default line**

```text
class: personal -> default: private, no-store; override: none permitted without an owner review
```

**2. New-path probe**

```text
request a route created after the change, with no hand-edited rule: if it lacks the directives, the default did not reach it
```

**3. Regression check**

```text
pipeline assertion: any route in the personal class must emit both tokens or the deploy fails
```

## Pitfalls

- Setting the default at the origin while an edge rule continues to override it
- Testing only routes that existed before the change, which cannot prove a default applies to new work
- Writing per-path rules when a class-level default would cover the whole surface

## Done when

- The class list is covered by a default and each class has a confirming response header
- A route added after the change emits the expected directives without hand configuration

## References

- [MDN - Cache-Control private and no-store](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
- [OWASP - Sensitive data protection](https://owasp.org/www-project-top-ten/)
