---
name: config-propagation-model-detection
description: "Work out whether edge configuration is pushed from a control plane or pulled from origin headers, because it decides who owns a fix and how fast a change takes effect. Use when the owner describes cache rules but the effective behaviour on a path contradicts what the origin sends"
pack: edgescout
version: 1.0.0
category: web-app
tags: [fingerprint, configuration, architecture]
---

# Config Propagation Model Detection

> Work out whether edge configuration is pushed from a control plane or pulled from origin headers, because it decides who owns a fix and how fast a change takes effect

**Use when:** the owner describes cache rules but the effective behaviour on a path contradicts what the origin sends

**Avoid when:** one configuration source is documented and its effect matches observed behaviour on every tested path

## Procedure

1. Pick a path where origin cache headers and observed storage disagree, and record both sides of the contradiction verbatim.
2. Check whether the disagreement follows a vendor rule pattern such as an override or a bypass list that only a control plane could apply.
3. Ask where the rule lives: dashboard, configuration repository, deployment pipeline or origin code, and note the answer's source.
4. Test propagation timing only if the owner permits a configuration change, otherwise record it as an open question for the owner.
5. Check whether different edge locations disagree, which would indicate a rollout that has not finished propagating.
6. Write a one-paragraph ownership statement saying which layer would have to change to alter the observed behaviour.

## Signals

- A path stores responses the origin explicitly marks as not storable
- The owner names a dashboard rule that contradicts a header seen in responses
- Two edge locations return different cache behaviour for an identical request
- A recent configuration change explains a behaviour shift seen between test sessions

## Patterns

**1. Contradiction record**

```text
path: /api/report
origin says: Cache-Control: no-store
observed: stored, age=118, status hit
conclusion: control-plane rule overrides origin directive
```

**2. Ownership statement**

```text
To change this behaviour, edit <layer> via <channel>; origin header changes alone would not take effect because the control-plane rule wins.
```

**3. Propagation note**

```text
If two locations disagree, record the timestamp of both observations and treat the configuration as mid-rollout rather than inconsistent by design
```

## Pitfalls

- Reporting an origin header fix when a control-plane rule would continue to override it
- Assuming configuration is pushed when a pull-based default silently applies vendor caching rules
- Calling a mid-rollout difference a bug and filing it before propagation had finished

## Done when

- Each tested path has a recorded contradiction or a confirmed alignment with its configuration source
- An ownership statement names the layer and channel that would change the behaviour

## References

- [OWASP - Cache control directives](https://cheatsheetseries.owasp.org/)
- [IETF RFC 9111 - Caching in HTTP](https://www.rfc-editor.org/rfc/rfc9111)
