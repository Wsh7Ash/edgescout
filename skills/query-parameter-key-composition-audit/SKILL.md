---
name: query-parameter-key-composition-audit
description: "Determine which query parameters separate stored copies and which are ignored, including the tracking and decoration parameters that frequently sit outside the key. Use when a path accepts query parameters and the key statement has not yet classified them as keyed or unkeyed"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, cache-key, query]
---

# Query Parameter Key Composition Audit

> Determine which query parameters separate stored copies and which are ignored, including the tracking and decoration parameters that frequently sit outside the key

**Use when:** a path accepts query parameters and the key statement has not yet classified them as keyed or unkeyed

**Avoid when:** the path is documented to ignore all query input and observed behaviour confirms one stored entry per path

## Procedure

1. Enumerate the parameters the application itself exposes through forms, links or documentation rather than guessing names.
2. For each parameter, issue two requests with different values and record whether the status token separates them.
3. Include a null value, an empty value and a reordered parameter list, because each shape can be normalized differently.
4. Check whether parameters that do not affect the rendered output are nevertheless keyed, which inflates storage rather than changing content.
5. Test whether a parameter is decoded once or twice at each layer, since a decode mismatch splits or merges entries unexpectedly.
6. Record a parameter table listing keyed, unkeyed, normalizing and unknown behaviour with one log line per verdict.

## Signals

- A parameter changes the rendered response while the status token stays identical across both values
- Two different values for one parameter share a single stored copy
- Parameter order or encoding changes the stored entry without changing the output
- A tracking parameter is ignored by the application but still splits the cache key

## Patterns

**1. Parameter table**

```text
param | values tested | status separates | body differs | verdict
id | 1,2 | no | yes | unkeyed and reflected
sort | asc,desc | yes | yes | keyed
utm_source | a,b | no | no | ignored and unkeyed
```

**2. Encoding triple**

```text
test the raw value, the percent-encoded value and the double-encoded value once each; a difference between them marks a decode mismatch between layers
```

**3. Storage inflation note**

```text
when a parameter is keyed but never changes output, record it as an entry-multiplier and flag it to the owner as a capacity concern
```

## Pitfalls

- Testing only well-formed values and missing the empty or repeated parameter case that behaves differently
- Assuming a tracking parameter is unkeyed because vendor defaults say so rather than because it was observed
- Overlooking that an unkeyed reflected parameter is exactly the shape a poisoning test needs

## Done when

- A parameter table covers every parameter the application exposes with a verdict per value shape
- Decode behaviour is recorded for at least the raw, encoded and double-encoded cases

## References

- [PortSwigger - Cache key confusion](https://portswigger.net/web-security/web-cache-poisoning)
- [IETF RFC 3986 - URI syntax](https://www.rfc-editor.org/rfc/rfc3986)
