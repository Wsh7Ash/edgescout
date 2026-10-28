---
name: non-destructive-probe-selection
description: "Choose request shapes that reveal caching behaviour without mutating state, so an edge assessment never leaves the property different from how it was found. Use when designing the request set for a cache or edge assessment where verbs, headers and query parameters can be varied"
pack: edgescout
version: 1.0.0
category: web-app
tags: [methodology, safety, probes]
---

# Non-Destructive Probe Selection

> Choose request shapes that reveal caching behaviour without mutating state, so an edge assessment never leaves the property different from how it was found

**Use when:** designing the request set for a cache or edge assessment where verbs, headers and query parameters can be varied

**Avoid when:** the engagement explicitly commissions state-changing tests and the owner has provided a disposable environment for them

## Procedure

1. Prefer GET and HEAD observations and treat any other verb as out of the default plan until a specific question requires it.
2. Vary one header or query dimension per request so an observed difference can be attributed to exactly one change.
3. Use cache-busting parameters only where the boundary permits them, and remove them from any request you intend to observe for storage.
4. Cap request rate at the ceiling from the boundary document and add a pause between probe families to keep logs readable.
5. Stop a probe family as soon as the behaviour is characterized rather than repeating it across every path.
6. Write down the exact request shape you used beside each response so a reviewer can reproduce without guessing.

## Signals

- A test set includes verbs that create, update or delete server state
- Two dimensions change in a single request, making the observed difference ambiguous
- Probe volume already exceeds the ceiling written in the boundary document
- Repeated identical requests are still running after the behaviour was clear

## Patterns

**1. One-dimension rule**

```text
Request N and request N+1 differ in exactly one field: one header, one query parameter, one path segment. Anything else invalidates the comparison.
```

**2. Verb whitelist**

```text
Default verbs: GET for body comparison, HEAD for header comparison. Every other verb needs a named question and an owner-approved environment.
```

**3. Rate note**

```text
log line: time, verb, path, changed_dimension, cache_status. If two lines share a timestamp with different dimensions, split them.
```

## Pitfalls

- Sending a state-changing verb to production while probing whether a response gets stored
- Bursting requests fast enough that rate limiting or a purge races your observation
- Reusing a session cookie across probes and losing the ability to separate identity from cache effects

## Done when

- The probe set uses only the approved verbs and varies one dimension per request
- Each recorded response has the request shape and the changed dimension written beside it

## References

- [PortSwigger - Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)
- [MDN - HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
