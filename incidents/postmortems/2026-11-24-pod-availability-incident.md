
# Incident Postmortem: Healthcare API Pod Availability

**Incident date:** November 24, 2026
**Environment:** AWS EKS — Canada Central (`ca-central-1`)
**Application:** Healthcare SRE Platform API
**Severity:** SEV-3 (portfolio exercise classification)
**Status:** Resolved
**Incident type:** Kubernetes workload availability

> This was a controlled portfolio incident simulation using synthetic healthcare data. It was not a real patient-care incident.

## 1. Executive Summary

A controlled failure scenario reduced the Healthcare API Deployment from two available replicas to one. The Prometheus metric exposed by kube-state-metrics detected the reduction, and the Grafana-managed alert transitioned from Pending to Alerting.

Grafana successfully delivered a notification to the in-cluster incident receiver. The receiver processed the webhook and returned HTTP 200.

The API was restored to two replicas. Prometheus subsequently reported 100% availability, and Grafana returned the alert to Normal.

## 2. Impact

- Desired API replicas: 2
- Available replicas during simulation: 1
- Observed replica availability: 50%
- Available replicas after recovery: 2
- Final observed availability: 100%

The simulation did not involve real patients, production services, or medical devices.

## 3. Detection

**Monitoring components:**
- Prometheus
- kube-state-metrics
- Grafana alerting

**Alert name:** `HealthcareAPI_PodAvailability_Low`

**Alert condition:**

```promql
100 *
kube_deployment_status_replicas_available{
  namespace="healthcare-dev",
  deployment="healthcare-api"
}
/
2
```

**Threshold:** Below 100%
**Evaluation interval:** 1 minute
**Pending period:** 2 minutes

## 4. Incident Timeline

| Time (November 24, 2026) | Event |
|---|---|
| 11:43:30 | Alert entered Pending at 50% availability |
| 11:45:30 | Alert transitioned to Alerting |
| During incident | Grafana notification delivered to incident receiver |
| During incident | Incident receiver processed webhook and returned HTTP 200 |
| Before 11:49:30 | API restored to two replicas |
| 11:49:30 | Alert returned to Normal at 100% availability |

Times are based on the Grafana alert history. Exact notification delivery time was not separately recorded.

## 5. Root Cause

The controlled test intentionally reduced the Kubernetes Deployment replica count from two to one:

```bash
kubectl scale deployment healthcare-api \
  --replicas=1 -n healthcare-dev
```

This reduced available replicas to 50%, triggering the configured alert.

This was an intentional simulation, not an unexpected application failure.

## 6. Response and Recovery

The API replica count was restored:

```bash
kubectl scale deployment healthcare-api \
  --replicas=2 -n healthcare-dev
```

Recovery was verified using:

```bash
kubectl get deployments,pods -n healthcare-dev -o wide
```

Final observed state:

- Healthcare API: 2/2 available
- Incident receiver: 1/1 available
- API pod restarts: 0
- Incident receiver pod restarts: 0
- Grafana alert state: Normal

## 7. What Went Well

- Prometheus detected reduced workload availability.
- Grafana transitioned through Pending and Alerting.
- The notification reached the in-cluster incident receiver.
- The incident receiver successfully processed the webhook.
- Kubernetes returned to the desired replica count.
- Grafana confirmed recovery by returning to Normal.

## 8. Improvement Opportunities

- Add automated tests for webhook parsing and runbook matching.
- Persist incident events instead of relying only on container logs.
- Add alert delivery failure monitoring.
- Introduce multi-window, multi-burn-rate SLO alerts.
- Add deployment rollback and failed rollout scenarios.
- Test node and availability-zone failure scenarios.
- Measure actual detection and recovery durations during future exercises.

## 9. Lessons Learned

Monitoring should cover both application-level symptoms and Kubernetes workload health. Alert delivery must be tested end to end, and recovery must be confirmed using both Kubernetes state and monitoring data.

Automated remediation should remain subject to human approval for actions that could affect service availability.

## 10. Evidence

Evidence collected during the exercise:

- Grafana alert history showing Pending, Alerting, and Normal.
- Incident receiver logs showing `POST /webhook` returning HTTP 200.
- Kubernetes deployment output showing two available API replicas.
- Kubernetes pod output showing healthy API and incident receiver workloads.

## 11. Final Outcome

**Result:** Successful controlled incident simulation.

The exercise demonstrated detection, alert evaluation, notification delivery, recovery, and post-incident verification in an AWS EKS environment.
