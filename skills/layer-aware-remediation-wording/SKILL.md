---
name: layer-aware-remediation-wording
description: "Write remediation steps against the layer that actually owns each change, so the receiving team can act without first untangling which component caused the defect. Use when an edge finding is ready to include remediation and more than one layer was involved in the behaviour"
pack: edgescout
version: 1.0.0
category: web-app
tags: [document, remediation, communication]
---

# Layer-Aware Remediation Wording

> Write remediation steps against the layer that actually owns each change, so the receiving team can act without first untangling which component caused the defect

**Use when:** an edge finding is ready to include remediation and more than one layer was involved in the behaviour

**Avoid when:** one single layer owns the whole behaviour and the fix is a one-line configuration change

## Procedure

1. Name the layer for each step: edge configuration, origin code, origin headers or network restriction.
2. State the expected effect of each step so a reader can verify the change worked rather than assume it did.
3. Order steps so that any prerequisite layer is corrected before dependent layers are touched.
4. Include a retest instruction for each step using the same pairing log that revealed the defect.
5. Mark steps that require a role or a maintenance window, since those need scheduling rather than a merge request.
6. List what was deliberately not changed, with the reason, so the reader knows the scope of the fix.

## Signals

- A remediation step names a header fix when a control-plane rule would continue to override it
- Steps carry no retest instruction, so closure cannot be verified
- A step requiring production access appears with no role or window requirement
- The report does not say which parts of the behaviour were left unchanged

## Patterns

**1. Step line**

```text
layer: edge config | change: drop x-original-url | effect: header no longer reaches origin | retest: reuse pairing log, expect unchanged body
```

**2. Order rule**

```text
fix the layer that wins the conflict first; correcting a subordinate layer while the winning rule remains changes nothing observable
```

**3. Not-changed list**

```text
unchanged: origin header parsing, because the edge drop covers it; recorded so the reader does not report it as an outstanding item
```

## Pitfalls

- Assigning every fix to the origin team when a control-plane rule is the deciding layer
- Omitting retest instructions, which makes an owner's closure claim unverifiable
- Hiding steps that need a maintenance window, so they are quietly dropped from the plan

## Done when

- Every remediation step names its layer, expected effect and retest instruction
- Unchanged items are listed with reasons so nothing is silently omitted

## References

- [OWASP - Defect remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-40 - Enterprise patch management](https://csrc.nist.gov/pubs/sp/800/40/r4/final)
