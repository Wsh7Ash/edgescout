---
name: purge-coverage-gap-analysis
description: "Check that the purge mechanism reaches every entry class the property relies on, because a purge that misses one class leaves revoked content served indefinitely. Use when the owner relies on purge for content removal and the purge scope or granularity has not been verified"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, purge, operations]
---

# Purge Coverage Gap Analysis

> Check that the purge mechanism reaches every entry class the property relies on, because a purge that misses one class leaves revoked content served indefinitely

**Use when:** the owner relies on purge for content removal and the purge scope or granularity has not been verified

**Avoid when:** policies use short lifetimes everywhere and content removal never depends on an explicit purge

## Procedure

1. Record the purge capabilities available: by URL, by prefix, by tag, by host and full flush, with who may trigger each.
2. For each tested path class, determine which purge type would actually clear it, including every variant entry.
3. Purge a synthetic test path where permission allows, then re-request every variant to confirm which entries cleared.
4. Check whether variants created by keyed dimensions survive a purge that targeted only the canonical URL.
5. Note propagation delay from purge request to observed miss, since a slow purge extends the revocation window.
6. Write a coverage table: path class, required purge type, confirmed effect, propagation delay.

## Signals

- A purge by canonical URL leaves keyed variants still reported as stored
- The team can purge only by host while content removal expectations assume per-path effect
- Propagation delay is long enough to matter for a revocation that must happen quickly
- Some content class can be purged only by a full flush nobody is authorized to trigger

## Patterns

**1. Coverage table**

```text
class | entry count | purge type needed | confirmed | delay
article | 3 variants | tag purge | no | -
asset | 1 entry | url purge | yes | 4s
```

**2. Variant sweep**

```text
after purge: re-request canonical, each keyed variant and one expired entry; report which three survived
```

**3. Authorization note**

```text
record who can trigger each purge type, because a capability nobody may use is not a capability the process has
```

## Pitfalls

- Purging the canonical URL and concluding coverage without checking the keyed variants
- Measuring propagation once and reporting it as a stable figure
- Recording a purge capability that exists in the vendor console but that no role is permitted to trigger

## Done when

- A coverage table lists every tested class with the purge type needed and the confirmed effect
- A purge test records canonical, variant and expired entry outcomes with the propagation delay

## References

- [IETF RFC 9111 - Invalidating stored responses](https://www.rfc-editor.org/rfc/rfc9111)
- [Akamapi - Cache purge options](https://techdocs.akamai.com/property-manager/docs/welcome-to-property-manager)
