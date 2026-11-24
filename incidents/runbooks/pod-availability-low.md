
# Runbook: Healthcare API Pod Availability Low

## 1. Alert Details

- Alert: HealthcareAPI_PodAvailability_Low
- Severity: Warning
- Category: Kubernetes Availability
- Namespace: healthcare-dev
- Deployment: healthcare-api
- Expected replicas: 2
- Trigger: Available replicas fall below 2

## 2. Incident Impact

Reduced replica availability may decrease application capacity and
resilience. If the remaining replica becomes unavailable, the API
may experience an outage.

This project uses synthetic healthcare data only.

## 3. Initial Investigation

Follow these steps in order.

### Step 1: Check deployment availability

kubectl get deployment healthcare-api -n healthcare-dev

Check:
- Desired replicas
- Ready replicas
- Available replicas
- Deployment conditions

### Step 2: Inspect pods

kubectl get pods -n healthcare-dev -l app=healthcare-api -o wide

Look for:
- CrashLoopBackOff
- OOMKilled
- ImagePullBackOff
- Pending
- Unexpected restarts

### Step 3: Inspect pod details

kubectl describe pods -n healthcare-dev -l app=healthcare-api

Check events, failed probes, scheduling failures and resource limits.

### Step 4: Review Kubernetes events

kubectl get events -n healthcare-dev --sort-by=.lastTimestamp

Look for:
- FailedScheduling
- FailedMount
- BackOff
- Unhealthy
- Insufficient CPU or memory

### Step 5: Inspect application logs

kubectl logs deployment/healthcare-api -n healthcare-dev --tail=100

If a specific pod is restarting, inspect its previous container logs:

kubectl logs <pod-name> -n healthcare-dev --previous

### Step 6: Check node health

kubectl get nodes

kubectl describe nodes

Look for:
- NotReady nodes
- MemoryPressure
- DiskPressure
- PIDPressure

## 4. Potential Root Causes

| Symptom | Possible cause |
|---|---|
| OOMKilled | Memory limit exceeded |
| CrashLoopBackOff | Application startup or runtime failure |
| ImagePullBackOff | Invalid image or ECR access issue |
| Pending | Insufficient resources or scheduling constraints |
| Failed probe | Application health endpoint failure |
| Node NotReady | Node or infrastructure issue |

These are diagnostic possibilities, not confirmed root causes.

## 5. Recovery Procedure

1. Identify the underlying failure.
2. Review recent deployments and configuration changes.
3. Correct the underlying issue.
4. Restore the expected replica count if appropriate.
5. Avoid repeatedly restarting pods without understanding the cause.
6. Verify both replicas become Ready.

## 6. Recovery Verification

kubectl get deployment healthcare-api -n healthcare-dev

kubectl get pods -n healthcare-dev -l app=healthcare-api -o wide

Confirm:
- Desired replicas: 2
- Available replicas: 2
- Both pods Ready
- No unexpected restarts

Check Prometheus availability:

up{namespace="healthcare-dev"}

Confirm the Grafana alert returns to Normal.

## 7. Escalation

Escalate to the platform SRE team if:
- Availability does not recover.
- Multiple nodes are unhealthy.
- Application failures persist after remediation.
- The incident affects other platform services.

Record the incident timeline, impact, root cause, recovery actions
and preventive improvements.

## 8. Safety

This platform uses synthetic healthcare data.

This runbook is for a demonstration SRE platform only. It is not
a certified medical platform and must never be used to operate
medical devices, modify insulin delivery, or direct patient treatment.
