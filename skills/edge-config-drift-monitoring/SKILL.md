---
name: edge-config-drift-monitoring
description: "Keep observed edge behaviour continuously compared with the declared key policy and storage policy, so a configuration drift is noticed before an incident reports it. Use when key and storage policies exist in writing but nothing currently checks that live behaviour still matches them"
pack: edgescout
version: 1.0.0
category: web-app
tags: [harden, monitoring, configuration]
---

# Edge Config Drift Monitoring

> Keep observed edge behaviour continuously compared with the declared key policy and storage policy, so a configuration drift is noticed before an incident reports it

**Use when:** key and storage policies exist in writing but nothing currently checks that live behaviour still matches them

**Avoid when:** an automated check already runs on every deploy and alerts on a mismatch

## Procedure

1. Choose a small sentinel set of paths covering each content class, including one personalized route and one asset route.
2. Capture the expected behaviour per sentinel: storage permitted, key dimensions present and directive set emitted.
3. Run the comparison on a schedule from a clean context and record any deviation from the expected behaviour.
4. Route each deviation to the owner of the layer responsible, since only that owner can correct it.
5. Add new content classes to the sentinel set as they appear, so coverage grows with the property.
6. Track deviations over time so a recurring drift is visible as a trend rather than a series of isolated alerts.

## Signals

- A sentinel path starts storing responses it was expected never to store
- An expected key dimension disappears from observed behaviour after a configuration deploy
- No scheduled check exists, so drift is only discovered when someone investigates an incident
- The sentinel set has not been updated since a new content class shipped

## Patterns

**1. Sentinel row**

```text
path: /account | class: personal | expect: no-store | expect key: cookie | last check: ok 2026-05-11
```

**2. Deviation line**

```text
sentinel: /account | expected no-store | observed public, max-age=60 | detected 2026-05-12 | owner: edge platform
```

**3. Coverage growth**

```text
every new content class must add a sentinel in the same change that introduces the class, otherwise the check silently loses ground
```

## Pitfalls

- Building a sentinel set that covers only public assets and never a personalized route
- Alerting on every deviation without routing it to the layer that owns the fix
- Never adding sentinels for new classes, so coverage shrinks relative to the application

## Done when

- A sentinel set covers every content class with expected storage, key and directive values
- A scheduled comparison runs and each deviation is routed to a named layer owner

## References

- [NIST SP 800-53 - Configuration management controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [OWASP - Security configuration review](https://owasp.org/www-project-application-security-verification-standard/)
