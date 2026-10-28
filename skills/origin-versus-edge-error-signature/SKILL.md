---
name: origin-versus-edge-error-signature
description: "Separate errors generated at the edge from errors returned by the origin, so an availability finding is attributed to the layer that actually produced it. Use when an error response appears during testing and the report must say which layer generated it"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, errors, attribution]
---

# Origin Versus Edge Error Signature

> Separate errors generated at the edge from errors returned by the origin, so an availability finding is attributed to the layer that actually produced it

**Use when:** an error response appears during testing and the report must say which layer generated it

**Avoid when:** the response carries a correlation id that the owner already maps to a single known layer

## Procedure

1. Capture the complete error response including status, headers and any body fingerprint, without attempting to influence the error further.
2. Compare its header set with a known-good response from the same host to see which vendor headers are missing or added.
3. Check whether the error carries an age or cache status token, which tells you whether the error itself was stored.
4. Repeat the same request once with a cache-busting parameter to see whether the origin reproduces the same error.
5. Note the correlation id or request id and ask the owner which layer logs it, since only one layer will have that record.
6. Record the attribution as edge-generated, origin-generated or stored-error, each with the evidence line that proves it.

## Signals

- The error body lacks the vendor header chain present on successful responses
- An error response carries an age value greater than zero
- The same error appears with and without a cache-busting parameter
- A vendor-branded error page shows no origin correlation id at all

## Patterns

**1. Attribution table**

```text
status | vendor headers | age | correlation id | attribution
503 | present | 0 | vendor-token | edge-generated
500 | present | 118 | origin-token | stored-error
502 | absent | 0 | none | origin-generated
```

**2. Bust compare**

```text
same path with and without a bust parameter: identical error body plus identical origin id means the origin produced it, not the edge
```

**3. Stored-error note**

```text
if age is above zero on an error, write that the error was replayed from storage and treat availability impact accordingly
```

## Pitfalls

- Reporting a vendor-generated maintenance page as an origin outage
- Treating a cached error as a live one and exaggerating the availability impact
- Concluding the origin is healthy because the edge served a stored success while origin fails

## Done when

- Every observed error is labelled edge-generated, origin-generated or stored-error with evidence
- At least one error class is confirmed by a cache-busted repeat request

## References

- [MDN - 502 Bad Gateway](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/502)
- [OWASP - Error handling and information leakage](https://owasp.org/www-project-web-security-testing-guide/)
