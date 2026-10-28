---
name: unkeyed-host-url-generation
description: "Detect when an unkeyed host or forwarded-host header reaches link generation, because stored absolute URLs turn one request into a poisonable shared response. Use when the key statement marks the host or a forwarded host header unkeyed and the application renders absolute URLs anywhere in the body"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, host-header, url-generation]
---

# Unkeyed Host URL Generation

> Detect when an unkeyed host or forwarded-host header reaches link generation, because stored absolute URLs turn one request into a poisonable shared response

**Use when:** the key statement marks the host or a forwarded host header unkeyed and the application renders absolute URLs anywhere in the body

**Avoid when:** the application renders only relative references and a body comparison confirms the host never appears in output

## Procedure

1. Enumerate the response regions that can contain an absolute URL: links, asset references, canonical tags, redirects and generated tokens.
2. Send two requests differing only in a forwarded host header while keeping every other dimension identical.
3. Compare those regions specifically rather than the whole body, since only the URL-bearing region matters for this check.
4. Check whether any observed change was stored by repeating the clean baseline request afterwards.
5. Verify whether the changed URL would be followed or rendered by a normal client, which sets the realistic impact.
6. Record the finding with the exact regions that changed and whether a stored copy retained the changed value.

## Signals

- A forwarded host header changes a link, asset path or canonical URL in the rendered body
- A redirect location is built from a header the edge does not include in the key
- The clean baseline after a header-varied request returns the changed URL from storage
- A generated token or callback URL embeds the forwarded host value

## Patterns

**1. Region diff**

```text
regions to compare: <a href>, <link href>, <script src>, <meta content>, location header; record only the changed region
```

**2. Baseline-after rule**

```text
after any header-varied request, re-request without the header: an unchanged baseline means no storage, a changed baseline means the copy was stored
```

**3. Impact sentence**

```text
the stored copy would make a normal client request <host> for an asset; write this sentence with the observed host value redacted to the scheme and registrable domain
```

## Pitfalls

- Reporting a reflected value that was never stored, which downgrades the finding to a response-splitting style observation
- Comparing full bodies and missing a two-character difference inside a long asset URL
- Describing impact without stating whether a normal client would actually follow the changed URL

## Done when

- URL-bearing regions are compared for every unkeyed host-style header tested
- A baseline-after request records whether any observed change was stored

## References

- [PortSwigger - Host header attacks](https://portswigger.net/web-security/host-header)
- [MDN - Forwarded header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Forwarded)
