---
name: personal-data-cache-scope
description: "Identify the endpoints whose responses contain personal, session-bound or tenant-specific data before testing, so shared-cache behaviour is never exercised against real user records. Use when any path can return account, billing, message or tenant data and the cache policy for those paths has not been verified"
pack: edgescout
version: 1.0.0
category: web-app
tags: [personal-data, privacy, scope]
---

# Personal Data Cache Scope

> Identify the endpoints whose responses contain personal, session-bound or tenant-specific data before testing, so shared-cache behaviour is never exercised against real user records

**Use when:** any path can return account, billing, message or tenant data and the cache policy for those paths has not been verified

**Avoid when:** the engagement target is exclusively static, public, non-tenant content with a documented shared cache policy

## Procedure

1. Walk the application's own navigation and API list to enumerate paths that return identifying, financial or tenant-specific fields.
2. Tag each path by data class: public, internal, personal, secret, since each class implies a different cache requirement.
3. Check the documented response headers for the personal and secret classes and record whether private or no-store is present.
4. Create synthetic test accounts and seed data you own, then use only those records for any shared-cache observation.
5. Note any path that mixes public and personal content in one response, because a single cache rule will apply to the whole body.
6. Mark the personal-class paths in the plan as observation-only: record headers, never serve one session's body to another.

## Signals

- A profile or billing route carries cache-control directives that allow shared storage
- Two tenants appear to share a route template differing only in an unkeyed segment
- Server-side rendering returns per-user markup on a path with a long freshness lifetime
- A response holding personal data omits the private directive entirely

## Patterns

**1. Class ladder**

```text
public -> may be stored in a shared cache when policy allows
internal -> team-readable, never shared
personal -> private, single user or session only
secret -> no-store, never written to any shared store
```

**2. Header expectation**

```text
Cache-Control: private, no-store for personal and secret classes; any value lacking those tokens is a finding, not a starting assumption of safety.
```

**3. Synthetic-only rule**

```text
Seed only accounts you control, and if a test would require reading another record to compare, stop and record the header evidence instead of the body.
```

## Pitfalls

- Comparing real user records to prove a shared-cache leak and turning a finding into a privacy incident
- Classifying a route by its URL pattern when the response is personalized by a cookie instead
- Assuming the absence of a caching header means shared storage is impossible

## Done when

- Every in-scope path carries a data class tag and an expected cache policy
- Only synthetic records owned by the tester appear in any recorded evidence

## References

- [OWASP - Sensitive data exposure](https://owasp.org/www-project-top-ten/)
- [MDN - Cache-Control private directive](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
