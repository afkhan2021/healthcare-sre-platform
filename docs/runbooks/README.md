# Operational Runbooks

This directory provides an index of operational procedures for the
Healthcare SRE Platform.

Runbooks support consistent incident investigation, recovery,
verification, and escalation.

## Available Runbooks

| Runbook | Alert | Severity | Description |
|---|---|---|---|
| [Healthcare API Pod Availability Low](../../incidents/runbooks/pod-availability-low.md) | HealthcareAPI_PodAvailability_Low | Warning | Investigate reduced Kubernetes pod availability and restore the expected replica count. |

## Incident Response Workflow

1. A monitoring alert identifies a potential service issue.
2. Review the corresponding runbook.
3. Investigate the affected Kubernetes resources and application logs.
4. Identify and address the underlying cause.
5. Verify service recovery using Kubernetes and Prometheus.
6. Document the incident, root cause, recovery actions, and improvements.

## Automation and Approval

The incident receiver can classify supported alerts and associate
them with relevant runbooks.

Remediation recommendations that require approval must be reviewed
and explicitly approved before execution.

## Safety and Scope

This project uses synthetic healthcare data only.

These runbooks are intended for demonstration and SRE engineering
purposes. They are not certified medical procedures and must never
be used to operate medical devices, modify insulin delivery, or
direct patient treatment.

## Contributing

When adding a runbook:

- Use a descriptive filename.
- Document alert details, severity, and potential impact.
- Include investigation and recovery procedures.
- Include recovery verification and escalation criteria.
- Document safety considerations.
- Add the runbook to this index.