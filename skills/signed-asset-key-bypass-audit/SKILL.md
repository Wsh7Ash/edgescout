---
name: signed-asset-key-bypass-audit
description: "Verify that time-limited signed asset access cannot be bypassed through a stored copy that outlives the signature it was fetched with. Use when the property serves signed URLs or signed cookies for protected assets behind a shared cache"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, signed-urls, access-control]
---

# Signed Asset Key Bypass Audit

> Verify that time-limited signed asset access cannot be bypassed through a stored copy that outlives the signature it was fetched with

**Use when:** the property serves signed URLs or signed cookies for protected assets behind a shared cache

**Avoid when:** protected assets are served with no-store so no shared copy can exist regardless of signing

## Procedure

1. Confirm how the signature is presented: query parameter, cookie or header, and record which of these the key includes.
2. Fetch a signed asset with a valid signature and record the storage directives and status token on the answer.
3. Repeat the request without the signature to see whether a stored copy is served to an unsigned client.
4. Check whether the signature parameter is excluded from the key while the response is still stored.
5. Verify that an expired signature cannot retrieve a stored copy, and record what the edge returns instead.
6. Report each case with the signature presentation, the key treatment and the observed unsigned or expired behaviour.

## Signals

- A stored asset answer returns for a request that presented no signature at all
- The signature parameter is excluded from the key while the protected response is stored
- An expired signature retrieves content that a valid signature originally fetched
- Two different signatures share one stored entry because neither is part of the key

## Patterns

**1. Signature table**

```text
presentation: query param
key includes: no
stored: yes
unsigned request: 200 from storage -> bypass observed
```

**2. Expiry probe**

```text
valid signature -> 200 stored; expired signature -> record status and body hash; identical hashes mean the copy was served regardless
```

**3. Expected result**

```text
unsigned or expired -> 403 or 404 from origin, never a stored 200 that a signature originally unlocked
```

## Pitfalls

- Testing expiry only with a still-valid signature and never waiting for or constructing an expired one
- Reporting a bypass when the asset was public all along and the signature was decorative
- Overlooking that a signature in a cookie may already be part of the key while one in a query parameter is not

## Done when

- A signature table records presentation, key treatment and storage for each protected class tested
- Unsigned and expired requests each have an observed status and body comparison

## References

- [AWS - Signed URLs and signed cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-urls.html)
- [OWASP - Insecure direct object references](https://owasp.org/www-project-web-security-testing-guide/)
