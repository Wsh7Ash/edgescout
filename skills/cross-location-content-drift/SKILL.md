---
name: cross-location-content-drift
description: "Check whether the same key returns different content at different edge locations, since drift means purges and deploys have not converged everywhere. Use when the property operates in multiple regions or the owner reports that changes appear unevenly across users"
pack: edgescout
version: 1.0.0
category: web-app
tags: [detect, consistency, operations]
---

# Cross-Location Content Drift

> Check whether the same key returns different content at different edge locations, since drift means purges and deploys have not converged everywhere

**Use when:** the property operates in multiple regions or the owner reports that changes appear unevenly across users

**Avoid when:** a single edge location serves all traffic and the owner confirms one deployment domain

## Procedure

1. Request the same key through each permitted entry point or region and record status, cache token and content fingerprint.
2. Compare the fingerprints across locations and record which locations agree and which diverge.
3. After an application-side change, repeat the comparison to see whether the change propagated everywhere.
4. Check whether a purge reached all locations or only the one where it was issued.
5. Note the time elapsed between issuing a change and every location reporting the new fingerprint.
6. Report drift with the diverging locations, the fingerprints and the convergence time actually observed.

## Signals

- Two locations return different fingerprints for the same key at the same time
- A purge issued in one location leaves others serving the previous content
- A deploy is visible on one region while another still returns the prior version
- Convergence takes longer than the team's stated rollout expectation

## Patterns

**1. Drift table**

```text
location | fingerprint | status | observed at
eu | a1f2 | hit | 09:12Z
us | 77bc | hit | 09:12Z  <- divergence
```

**2. Convergence note**

```text
change issued 09:10Z, all locations agree 09:14Z -> 4 minutes observed, recorded as the actual rollout window
```

**3. Purge reach**

```text
purge issued at one location: re-request the same key at every location and record which returned a miss
```

## Pitfalls

- Measuring drift once and treating a mid-rollout snapshot as a permanent inconsistency
- Comparing locations at different times and blaming propagation for a difference caused by timing
- Reporting drift without the convergence measurement that would tell the owner how large it really is

## Done when

- A drift table records fingerprint, status and timestamp for every location tested
- A convergence time is measured after a change or purge rather than estimated

## References

- [Cloudflare - Cache propagation across locations](https://developers.cloudflare.com/cache/)
- [IETF RFC 9111 - Cache coherence expectations](https://www.rfc-editor.org/rfc/rfc9111)
