---
name: verb-handling-in-shared-storage
description: "Audit which HTTP verbs the edge stores and replays, because a stored write or a replayed read for the wrong verb breaks application semantics for every later client. Use when the boundary permits non-idempotent verb observation and the edge may be storing responses by more than the request line"
pack: edgescout
version: 1.0.0
category: web-app
tags: [audit, verbs, shared-cache]
---

# Verb Handling in Shared Storage

> Audit which HTTP verbs the edge stores and replays, because a stored write or a replayed read for the wrong verb breaks application semantics for every later client

**Use when:** the boundary permits non-idempotent verb observation and the edge may be storing responses by more than the request line

**Avoid when:** the engagement restricts testing to GET and HEAD and the owner confirms other verbs bypass the cache entirely

## Procedure

1. Confirm from the rules of engagement which verbs may be sent and which must remain untouched.
2. For each permitted verb, record the cache status token and whether a stored copy exists for the same path.
3. Test whether a stored GET answer is returned for a request that used another verb on the same path.
4. Check whether a state-changing verb's response carries storage-permitting directives at all.
5. Verify that a purge of the path clears every verb's entry, not just the one you observed.
6. Record the verb matrix: verb, stored, replayed, purge effect, with the status token for each cell.

## Signals

- A response to a state-changing verb carries directives that permit shared storage
- A second verb on the same path receives the answer stored for a GET request
- Purging one path leaves other verbs' answers still reported as stored
- A caching status token appears on a response that should never be stored

## Patterns

**1. Verb matrix**

```text
verb | stored | replayed | purge clears
GET | yes | yes | yes
HEAD | yes | yes | yes
POST | flagged | no | unknown
```

**2. Permit rule**

```text
state-changing verb + storage-permitting directive -> record as a policy defect even when no replay was observed
```

**3. Purge scope note**

```text
purge the path once with permission, then re-request every tested verb to see which entries survived
```

## Pitfalls

- Sending a state-changing verb purely to fill a matrix cell when the boundary forbids it
- Concluding an entry was purged without re-requesting every verb for that path
- Reporting a stored HEAD as a stored GET, since the two behave differently for body comparison

## Done when

- A verb matrix records stored, replayed and purge behaviour for every permitted verb
- State-changing verbs are either tested under explicit permission or explicitly marked untested

## References

- [IETF RFC 9110 - HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [MDN - HTTP methods overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
