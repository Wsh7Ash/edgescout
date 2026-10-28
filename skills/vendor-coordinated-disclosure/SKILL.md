---
name: vendor-coordinated-disclosure
description: "Route an edge defect to the party that can actually fix it, whether that is the property owner or the edge vendor, and set a disclosure timeline that both can meet. Use when a finding involves a third-party edge vendor's own configuration or product behaviour"
pack: edgescout
version: 1.0.0
category: web-app
tags: [document, disclosure, coordination]
---

# Vendor Coordinated Disclosure

> Route an edge defect to the party that can actually fix it, whether that is the property owner or the edge vendor, and set a disclosure timeline that both can meet

**Use when:** a finding involves a third-party edge vendor's own configuration or product behaviour

**Avoid when:** the defect is entirely in the owner's configuration and needs no vendor involvement

## Procedure

1. Decide the fixing party from the layer attribution: owner configuration, owner code, or vendor product behaviour.
2. Prepare the report with the evidence pack and the reproduction recipe, redacted to remove tenant content entirely.
3. Send it first to the property owner, since they hold the relationship and the contractual path to the vendor.
4. Agree a timeline: acknowledgement, target fix date and a disclosure date, recorded in writing.
5. Re-test after the fix lands using the same recipe, and record whether the behaviour actually changed.
6. Close with a note on what remains open, including any item that depends on a vendor release you do not control.

## Signals

- The defect requires a change only the edge vendor can make to their product
- The report reaches the vendor before the owner has seen it, breaking the agreed channel
- No re-test was performed after the fix was announced
- Items remain open with no owner and no date attached

## Patterns

**1. Routing line**

```text
defect: control-plane rule applied by vendor default | fixing party: owner config first, vendor product second | channel: owner to vendor
```

**2. Timeline block**

```text
ack by <date> | fix target <date> | re-test <date> | disclosure <date> -> written and confirmed by both sides
```

**3. Closure note**

```text
re-tested with published recipe at <timestamp>: behaviour changed from <before token> to <after token> -> item closed
```

## Pitfalls

- Contacting a vendor directly about a defect that is really the owner's configuration choice
- Publishing tenant content in a report that will be retained by a vendor portal indefinitely
- Announcing closure without a re-test that shows the behaviour actually changed

## Done when

- The fixing party and channel are named, with a timeline confirmed in writing
- A re-test after the fix records the before and after status tokens for each closed item

## References

- [ISO 29147 - Vulnerability disclosure guidance](https://www.iso.org/standard/72311.html)
- [OWASP - Coordinated disclosure](https://owasp.org/www-project-vulnerability-disclosure/)
