---
name: cache-control-override-conflict
description: "Find places where the effective storage policy differs from what the origin sent, because a silently overridden directive is where unintended storage begins. Use when observed storage behaviour contradicts the cache directives the origin attaches to a response"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, headers, policy]
---

# Cache-Control Override Conflict

> Find places where the effective storage policy differs from what the origin sent, because a silently overridden directive is where unintended storage begins

**Use when:** observed storage behaviour contradicts the cache directives the origin attaches to a response

**Avoid when:** the origin's directives and the observed storage window agree on every tested path

## Procedure

1. Record the origin's cache directives verbatim for each tested path together with the observed storage behaviour.
2. Classify the relationship: honoured, tightened by the layer, or weakened by the layer, with one line per path.
3. Where the layer weakened the directive, ask whether a control-plane rule exists and note where it lives.
4. Check both directions of conflict: a no-store the edge ignores, and a public the edge refuses to store.
5. Note conflicts that differ between content classes, since one rule may apply to assets and another to application routes.
6. Summarize each conflict as an ownership item: which layer must change for the two sides to agree.

## Signals

- A response marked no-store still shows an age value on a later request
- A response marked public is never stored on a path where assets are normally cached
- s-maxage and max-age disagree and the layer honours neither
- One content class follows the origin while another is overridden by a rule

## Patterns

**1. Conflict line**

```text
path | origin says | observed | classification | owner
/api | no-store | stored, age=118 | weakened | control-plane rule
```

**2. Both-direction test**

```text
always test a restrictive directive and a permissive one on the same host, because a single rule can cause either direction of conflict
```

**3. Ownership handoff**

```text
the fix belongs to whoever edits <layer>; note this explicitly so the report does not tell the origin team to change a header that is ignored
```

## Pitfalls

- Reporting the conflict to the wrong team when a control-plane rule is the actual source
- Testing only restrictive directives and missing a permissive directive the layer refuses
- Assuming a conflict is intentional when no one on the team can name the rule that produces it

## Done when

- Every tested path has a conflict classification of honoured, tightened or weakened
- Each conflict names the layer that owns the fix rather than only the symptom

## References

- [IETF RFC 9111 - Cache-control directives](https://www.rfc-editor.org/rfc/rfc9111)
- [MDN - Cache-Control header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
