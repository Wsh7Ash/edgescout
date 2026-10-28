---
name: cache-key-duplication-splitting
description: "Find dimensions that split one logical resource into many stored entries, which raises origin load and storage cost and can hide a purge behind an entry you never saw. Use when the key statement lists dimensions that do not change output but still create separate stored entries"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, capacity, cache-key]
---

# Cache Key Duplication Splitting

> Find dimensions that split one logical resource into many stored entries, which raises origin load and storage cost and can hide a purge behind an entry you never saw

**Use when:** the key statement lists dimensions that do not change output but still create separate stored entries

**Avoid when:** the owner confirms every keyed dimension changes the response body or headers

## Procedure

1. List every keyed dimension from the key statement and mark whether it changes the response in your observations.
2. Quantify the split for one representative path by varying each non-contributing dimension and counting distinct entries.
3. Check whether tracking or decoration parameters are included in the key while the application ignores them.
4. Note whether the split is bounded by a rule or unbounded, since an unbounded set grows with request volume.
5. Estimate the practical effect: additional origin requests per visitor and the purge surface that now covers more entries.
6. Report the split with the counted entries and the responsible configuration rule, recommending key exclusion for non-contributing dimensions.

## Signals

- Adding a tracking parameter creates a new stored entry without changing the response
- The same resource exists in many entries differing only by a parameter the application never reads
- Origin request logs show repeated fetches for one path with varying parameter values
- A purge by path leaves sibling entries still reported as stored

## Patterns

**1. Split count**

```text
path /article with 6 tracking values -> 6 stored entries, identical bodies, origin fetched 6 times
```

**2. Bounded check**

```text
is the varying set finite, such as language, or unbounded, such as client-supplied identifiers? write which one applies to this path
```

**3. Recommendation line**

```text
exclude <dimension> from the key under rule <rule-name>; it never changes the response and multiplying entries increases origin traffic
```

## Pitfalls

- Treating a capacity concern as a security finding and overstating its impact class
- Counting entries from an unbounded parameter set without saying the count is an estimate
- Recommending key exclusion without noting that the dimension must first be proven non-contributing

## Done when

- A counted split example records entries for one path and the dimension responsible
- The recommendation names the configuration rule to change and the precondition proven first

## References

- [IETF RFC 9111 - Constructing cache keys](https://www.rfc-editor.org/rfc/rfc9111)
- [Cloudflare - Cache key configuration](https://developers.cloudflare.com/cache/)
