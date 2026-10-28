---
name: cache-key-composition-probing
description: "Infer which request dimensions make up the cache key by varying one dimension at a time and observing whether the served copy changes. Use when the key composition of an in-scope path is undocumented and later tests depend on knowing what separates two stored copies"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, cache-key, methodology]
---

# Cache Key Composition Probing

> Infer which request dimensions make up the cache key by varying one dimension at a time and observing whether the served copy changes

**Use when:** the key composition of an in-scope path is undocumented and later tests depend on knowing what separates two stored copies

**Avoid when:** the owner supplies a key configuration from their vendor console or infrastructure-as-code repository

## Procedure

1. Establish a baseline: fetch the path with no added parameters twice and confirm both answers carry the same cache status and body.
2. Vary one dimension at a time and record whether the status token changes, which reveals whether that dimension separated the lookup.
3. Test candidate dimensions in this order: path, query parameters as a set, individual query parameters, host, then selected headers.
4. Include headers commonly used for content negotiation, such as accept and accept-language, because they frequently sit outside the key.
5. For each dimension, note whether a different body, a different status or neither result indicates keyed or unkeyed behaviour.
6. Write a key composition statement naming every dimension you proved keyed and every dimension you proved unkeyed.

## Signals

- Changing a query parameter returns the identical stored body and status token
- Two paths differing only in a trailing separator share one stored copy
- An accept-language change alters the body while the status token stays a hit
- A dimension you expected to be keyed produces no observable difference at all

## Patterns

**1. Key statement**

```text
keyed: scheme, host, path, query-set
unkeyed: accept-language, x-forwarded-host, utm params
unknown: cookie, authorization
```

**2. Pairing log**

```text
dimension | request A status/body | request B status/body | verdict
query ?a=1 vs ?a=2 | hit/identical | hit/identical | unkeyed
accept-language en vs fr | hit/body-x | hit/body-y | keyed
```

**3. Unknown reserve**

```text
Dimensions whose behaviour cannot be observed safely stay marked unknown and get a conservative assumption in the audit phase.
```

## Pitfalls

- Changing two dimensions in one request and attributing the difference to whichever one you were thinking about
- Assuming a dimension is keyed because it is named in vendor documentation rather than in observed behaviour
- Forgetting that an unkeyed dimension which changes the response is the precondition for a poisoning finding

## Done when

- A key statement lists every dimension proved keyed, unkeyed or unknown
- Each verdict is backed by a paired request log line with both status tokens

## References

- [PortSwigger - Web cache poisoning fundamentals](https://portswigger.net/web-security/web-cache-poisoning)
- [IETF RFC 9111 - Vary and cache keys](https://www.rfc-editor.org/rfc/rfc9111)
