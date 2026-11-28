
# Exercise 02: Healthcare API Outage and SLO Burn

## Objective

Simulate a Healthcare API outage or severe degradation, investigate its impact using service-level indicators (SLIs), assess error-budget consumption, and restore service.

Skills demonstrated:

- SLI, SLO, and error-budget analysis.
- Prometheus alert interpretation.
- Incident triage and impact assessment.
- Service recovery and validation.
- Blameless post-incident review.

## 1. Scenario

The Healthcare API begins returning HTTP 5xx errors or experiencing increased latency.

Customers may experience failed or delayed API requests.

Prometheus evaluates availability, error rate, and latency indicators. Depending on the severity and duration, SLO alerts may fire.

## 2. Service Objectives

The platform defines these objectives:

| Indicator | Objective |
|---|---|
| Availability | 99.9% |
| HTTP 5xx error rate | At most 0.1% |
| Latency | At least 95% of measured requests within 300ms |

A 99.9% SLO has a time-based equivalent of approximately 43.8 minutes over a 30-day month. However, this platform measures availability using eligible requests, so actual error-budget consumption is request-based rather than calculated directly from downtime minutes.

HTTP 4xx client errors are excluded from eligible availability requests.

## 3. Detection and Alerting

The following Prometheus alerts are configured:

| Alert | Condition | Pending |
|---|---|---|
| HealthcareAPIAvailabilityFastBurn | Error-budget burn above 14.4x over 5m and 1h | 2m |
| HealthcareAPIAvailabilitySlowBurn | Error-budget burn above 6x over 30m and 6h | 15m |
| HealthcareAPILatencySLOBreach | Less than 95% within 300ms | 10m |
| HealthcareAPIErrorRateSLOBreach | HTTP 5xx rate above 0.1% | 5m |

Recording rules used:

- healthcare_api:availability:ratio5m
- healthcare_api:availability:ratio30m
- healthcare_api:availability:ratio1h
- healthcare_api:availability:ratio6h
- healthcare_api:error_rate:ratio5m
- healthcare_api:latency_within_300ms:ratio5m

## 4. Incident Response

### Step 1: Acknowledge and assess

- Identify the firing alert and severity.
- Determine the affected service and namespace.
- Establish the incident start time.
- Check whether the issue affects all requests or a subset.
- Review recent deployments and configuration changes.

### Step 2: Investigate the application

Inspect workload status:

    kubectl get deployments,pods -n healthcare-dev

Inspect application events:

    kubectl get events -n healthcare-dev --sort-by='.lastTimestamp'

Inspect application logs:

    kubectl logs deployment/healthcare-api -n healthcare-dev --tail=100

Check container restart counts and resource usage:

    kubectl describe deployment healthcare-api -n healthcare-dev

### Step 3: Investigate service-level indicators

In Prometheus, inspect:

    healthcare_api:availability:ratio5m

    healthcare_api:error_rate:ratio5m

    healthcare_api:latency_within_300ms:ratio5m

Compare short-window and long-window availability indicators to distinguish a sudden incident from sustained degradation.

### Step 4: Identify the likely cause

Investigate possible causes:

- Application regression or defective deployment.
- Insufficient pod capacity.
- Container crashes or repeated restarts.
- Resource exhaustion.
- Network or service connectivity problems.
- Downstream dependency failures.

Record evidence before selecting a mitigation.

## 5. Mitigation and Recovery

Select a mitigation appropriate to the confirmed cause.

Examples:

- Roll back a defective application release.
- Restore the intended replica count.
- Correct an application configuration issue.
- Resolve resource pressure.
- Restore an unavailable dependency.

If replica reduction is confirmed as the cause, restore the expected replica count:

    kubectl scale deployment healthcare-api --replicas=2 -n healthcare-dev

Verify the rollout:

    kubectl rollout status deployment/healthcare-api -n healthcare-dev

Verify pod readiness:

    kubectl get pods -n healthcare-dev

Do not apply a mitigation without confirming that it is appropriate for the incident.

## 6. Recovery Validation

Confirm:

- Expected application replicas are available.
- Pods are Running and Ready.
- Health and readiness checks succeed.
- HTTP 5xx errors return to acceptable levels.
- Availability SLI recovers.
- Latency objective is met.
- Relevant alerts return to Normal.

Recovery should be based on observed metrics and service health, not simply the disappearance of an alert.

## 7. Error-Budget Assessment

Calculate the remaining monthly error budget using the observed availability SLI.

For a 30-day period:

- Total monthly budget: approximately 43.8 minutes.
- Availability objective: 99.9%.
- Error-budget consumption: (100 - observed availability percentage) / 0.1 x 100.

Assess whether the incident warrants:

- Release restrictions.
- Additional reliability work.
- Capacity improvements.
- Stronger testing or deployment safeguards.

## 8. Post-Incident Review

Document:

- Incident timeline.
- Customer or service impact.
- Detection method.
- Root cause and contributing factors.
- Mitigation and recovery actions.
- Time to detect and time to recover.
- Error-budget impact.
- Preventive actions, owners, and follow-up dates.

Keep the review blameless and focus on improving system reliability.

## 9. Exercise Safety and Status

This exercise uses synthetic application data.

The previous AWS EKS development cluster has been destroyed. Commands are documented for a future isolated development or local Kubernetes environment.

**Status:** Documented; execution pending.

No live outage simulation or recovery is claimed.
