---
name: set-cookie-on-cacheable-response
description: "Find responses that both set a cookie and allow shared storage, since a replayed Set-Cookie header can hand one client another client's session state. Use when any in-scope response carries a Set-Cookie header together with storage-permitting cache directives"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, cookies, shared-cache]
---

# Set-Cookie on Cacheable Response

> Find responses that both set a cookie and allow shared storage, since a replayed Set-Cookie header can hand one client another client's session state

**Use when:** any in-scope response carries a Set-Cookie header together with storage-permitting cache directives

**Avoid when:** the response marks itself private or no-store, so a shared cache must never store it

## Procedure

1. Capture the full response for each path that sets a cookie and record the cache directives alongside it.
2. Flag any response where Set-Cookie coexists with a directive that permits shared storage.
3. Repeat the request without a cookie jar to see whether the stored copy replays the Set-Cookie header to a fresh client.
4. Inspect the cookie attributes on the flagged responses: scope, path, secure, same-site and any session lifetime.
5. Check whether a purge or expiry removes the replayed cookie promptly, or whether it persists for the whole freshness lifetime.
6. Record each case with the directive set, the cookie attributes and the replay observation from a clean client.

## Signals

- Set-Cookie appears on a response the edge reports as stored
- A request with no prior cookie receives a Set-Cookie header served from storage
- The cookie carries a broad scope while the response caching allows any client to receive it
- The replayed cookie survives longer than the application intended the session to live

## Patterns

**1. Flag rule**

```text
set-cookie present AND cache-control lacks private and lacks no-store -> flag for replay test
```

**2. Clean-client probe**

```text
empty cookie jar, same URL, note whether set-cookie returns with an age above zero; age above zero means a stored copy delivered it
```

**3. Attribute record**

```text
name scope path secure same-site lifetime -> written beside the flag so impact is judged from the cookie, not the header alone
```

## Pitfalls

- Reporting a cookie replay without checking whether the response was actually stored rather than regenerated
- Judging impact from the header alone without reading the cookie scope and lifetime
- Missing a path that sets a session cookie on a public asset such as a tracking pixel

## Done when

- Every response with Set-Cookie and storage-permitting directives has a clean-client replay observation
- Cookie attributes are recorded beside each flag so impact can be judged

## References

- [MDN - Set-Cookie header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)
- [OWASP - Session fixation and cookie security](https://cheatsheetseries.owasp.org/)
