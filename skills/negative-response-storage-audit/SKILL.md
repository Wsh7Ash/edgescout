---
name: negative-response-storage-audit
description: "Audit whether error and empty responses are stored and replayed, since a cached failure turns one origin hiccup into an outage that outlives its cause. Use when error statuses appear during testing or the property serves content that can legitimately disappear between requests"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, errors, availability]
---

# Negative Response Storage Audit

> Audit whether error and empty responses are stored and replayed, since a cached failure turns one origin hiccup into an outage that outlives its cause

**Use when:** error statuses appear during testing or the property serves content that can legitimately disappear between requests

**Avoid when:** the owner confirms errors are excluded from storage by rule and a repeat request proves no error is stored

## Procedure

1. Record the cache status token and directives on each error class observed during the engagement.
2. Trigger a controlled, non-destructive error such as a not-found path and check whether the answer is stored.
3. Re-request the same path after the error was produced and note whether storage or a live origin answer is returned.
4. Check whether an error response carries a long freshness lifetime while the successful responses on the host use short ones.
5. Verify what a purge or a recovery at the origin does to a stored error: does it clear, or must it expire naturally?
6. Report each stored-error case with its status, lifetime, and the recovery behaviour observed.

## Signals

- An error response carries an age value greater than zero on a later request
- A transient failure is still being served after the origin recovered
- The error's freshness lifetime exceeds the lifetime the origin sets for successful responses
- A purge does not clear a stored error while clearing the success entry on the same path

## Patterns

**1. Error storage line**

```text
status=503 age=42 cache-control=max-age=300 -> stored for 300s after the transient cause
```

**2. Recovery check**

```text
wait for origin recovery, then re-request: a stored error still returned means availability impact continues past the cause
```

**3. Lifetime compare**

```text
error lifetime vs success lifetime on the same host; a longer error lifetime is the reportable asymmetry
```

## Pitfalls

- Triggering an error in a way that stresses the origin rather than a controlled not-found path
- Reporting a stored error without checking whether a purge or expiry clears it
- Comparing lifetimes across different hosts instead of within the same host

## Done when

- Each observed error class has a status, age and lifetime recorded
- Recovery behaviour is confirmed by a request after the transient cause ended

## References

- [IETF RFC 9111 - Freshness and error handling](https://www.rfc-editor.org/rfc/rfc9111)
- [MDN - 503 Service Unavailable](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/503)
