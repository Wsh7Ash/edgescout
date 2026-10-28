---
name: authenticated-response-shared-storage
description: "Check whether identity-bound responses can be stored in a cache that serves other users, which is the highest-impact outcome a shared cache can produce. Use when a path returns different content per session or account and the response does not clearly mark itself as private"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, authentication, shared-cache]
---

# Authenticated Response Shared Storage

> Check whether identity-bound responses can be stored in a cache that serves other users, which is the highest-impact outcome a shared cache can produce

**Use when:** a path returns different content per session or account and the response does not clearly mark itself as private

**Avoid when:** the response carries private or no-store and a repeat request from a second session confirms isolation

## Procedure

1. Create two synthetic sessions you own and request the same authenticated path with each, recording the full header set both times.
2. Check both responses for private, no-store and no-cache, and note any of them missing from a response that carries per-session content.
3. Confirm the key statement includes whichever identity dimension the origin uses, such as cookie or authorization.
4. Ask for the path once without any credentials to see whether an unauthenticated answer is stored and then replayed to a signed-in client.
5. Verify isolation by alternating the two sessions several times rather than trusting a single successful pair.
6. Record the verdict with the header evidence and the alternation log, using only your own synthetic accounts.

## Signals

- An authenticated response omits private and no-store while containing account-specific content
- The key statement does not include the identity header the origin uses to select content
- A signed-in client receives content that matches a different session's earlier request
- An unauthenticated request is answered from storage with content that belongs to a session

## Patterns

**1. Isolation log**

```text
session A -> 200 body-A, status hit, cache-control: public, max-age=60
session B -> 200 body-A  <- body-B expected, mismatch recorded
```

**2. Header expectation**

```text
authenticated + personalized -> Cache-Control: private, no-store; anything else on this class is a finding
```

**3. No-credential probe**

```text
request with no identity header at all: if the answer comes from storage, the stored entry was not partitioned by identity
```

## Pitfalls

- Using two real user accounts and turning an isolation test into a privacy incident
- Testing once and concluding isolation when the store may simply have been cold the first time
- Forgetting an unauthenticated request, which is often the case where the mismatch first appears

## Done when

- Two synthetic sessions alternate several times with the header sets recorded for both
- A verdict of isolated or shared is backed by the alternation log and the observed directives

## References

- [OWASP - Session management testing](https://owasp.org/www-project-web-security-testing-guide/)
- [IETF RFC 9111 - Storing responses in shared caches](https://www.rfc-editor.org/rfc/rfc9111)
