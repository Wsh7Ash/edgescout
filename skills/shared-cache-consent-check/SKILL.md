---
name: shared-cache-consent-check
description: "Confirm that shared caching of the tested content is contractually allowed, since caching a response you were not permitted to share changes the incident class entirely. Use when the property sits behind a third-party cache and terms of service, an enterprise agreement or a data-processing addendum may restrict storage"
pack: edgescout
version: 1.0.0
category: web-app
tags: [consent, cdn, privacy]
---

# Shared Cache Consent Check

> Confirm that shared caching of the tested content is contractually allowed, since caching a response you were not permitted to share changes the incident class entirely

**Use when:** the property sits behind a third-party cache and terms of service, an enterprise agreement or a data-processing addendum may restrict storage

**Avoid when:** the owner confirms in writing that all in-scope content is public and may be stored and replayed by any intermediary

## Procedure

1. Read the program terms for words such as cache, store, replicate, archive and intermediary, and quote each sentence that touches storage.
2. Ask whether third-party edge storage of test content is expected behaviour for the property under the current agreement.
3. Check whether the agreement restricts the geographic regions where responses may be stored during the assessment.
4. Note any content class the owner marks as non-cacheable by policy even where no header enforces it yet.
5. Carry the answer into the plan: shared-cache observations are permitted only for classes the owner explicitly cleared.
6. Record the consent answer next to your boundary document so a later reader can see why certain tests were skipped.

## Signals

- Terms mention data residency while the edge provider operates in other regions
- The owner states a no-cache policy that no response header currently enforces
- A data-processing addendum lists caching as a sub-processor activity to review
- Test content is being replicated to regions the agreement does not cover

## Patterns

**1. Consent matrix**

```text
content class | storage permitted | region limit | source
public docs | yes | none | terms section 4
account pages | no | none | owner reply 2026-05-11
tenant reports | no | region-limited | dpa annex b
```

**2. Silence handling**

```text
Absence of a restriction is not consent. Record consent as unknown and limit yourself to header observation until an owner reply resolves it.
```

**3. Skip note**

```text
When a test is skipped for consent reasons, write one line naming the test, the class and the consent source so the gap is visible in the report.
```

## Pitfalls

- Treating public availability as permission to have content stored and replayed by a third party
- Running a shared-cache observation against a class the owner listed as non-cacheable
- Reaching a consent conclusion from a general privacy policy rather than the engagement terms

## Done when

- A consent matrix records storage permission and region limits per content class
- Skipped tests appear in the report with the consent reason attached

## References

- [OWASP - Privacy and data protection considerations](https://owasp.org/www-project-application-security-verification-standard/)
- [IETF RFC 9111 - HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)
