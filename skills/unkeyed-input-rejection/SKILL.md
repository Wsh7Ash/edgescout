---
name: unkeyed-input-rejection
description: "Make the edge and the origin ignore untrusted input that never participates in the key, closing the path between a reflected header and a stored shared response. Use when an unkeyed header was proven to influence the response during the audit phase"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, headers, defense]
---

# Unkeyed Input Rejection

> Make the edge and the origin ignore untrusted input that never participates in the key, closing the path between a reflected header and a stored shared response

**Use when:** an unkeyed header was proven to influence the response during the audit phase

**Avoid when:** every header that influences output is already part of the key and the response is marked private

## Procedure

1. List the specific headers proven unkeyed and influential, and write each one down by its exact name.
2. Configure the edge to drop or override those headers before the request reaches the application.
3. Configure the origin to reject or normalize the same headers independently, since one layer alone is not a durable fix.
4. Re-run the original pairing test that first revealed the influence and confirm the response no longer changes.
5. Add the rejection to configuration-as-code so the fix survives a dashboard reset or a rebuild.
6. Record the retest result with the original pairing log so the closure is provable rather than asserted.

## Signals

- A header known to be unkeyed still reaches the application after the first fix attempt
- Only the edge drops the header while the origin continues to honour it
- The fix lives only in a console and disappears on the next configuration deploy
- The original pairing test still produces a differing response after the change

## Patterns

**1. Rejection record**

```text
header | layer | action | retest result
x-original-url | edge | drop | response unchanged
x-original-url | origin | reject | response unchanged
```

**2. Retest rule**

```text
reuse the exact pairing log from the finding; a retest that changes any other dimension does not close the item
```

**3. Code placement**

```text
the rejection belongs in the configuration repository or the origin middleware, not only in a console, so a rebuild keeps it
```

## Pitfalls

- Fixing only one layer and assuming the other will never be reached directly
- Retesting with a different request shape and declaring closure from a different experiment
- Leaving the fix in a console configuration that a routine deploy overwrites

## Done when

- Every header from the finding has a rejection recorded at each layer that receives it
- The original pairing retest shows an unchanged response and the retest log is attached

## References

- [OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/)
- [PortSwigger - Cache poisoning remediation](https://portswigger.net/web-security/web-cache-poisoning)
