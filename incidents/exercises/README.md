# Incident Simulation Exercises

These exercises demonstrate incident detection,
troubleshooting, recovery, and prevention for the
Healthcare SRE Platform.

All scenarios use synthetic application data.

## Exercises

| Exercise | Failure Mode | Key SRE Skills |
|---|---|---|
| 01 | CrashLoopBackOff | Container troubleshooting, Kubernetes events, recovery |
| 02 | Healthcare API outage | SLIs, SLOs, error budgets, incident response |
| 03 | Failed deployment | Rollout monitoring, rollback, release safety |

## Execution Environment

The exercises are designed for an isolated development
Kubernetes environment.

Do not execute failure-injection commands against
production or shared clusters.

The current repository contains the exercise definitions.
A live Kubernetes cluster is required to execute the
Kubernetes failure-injection scenarios.

## Evidence to Capture

For each exercise, record:

- Failure injection and expected symptoms.
- Detection method and relevant alerts.
- Investigation commands and findings.
- Root cause.
- Recovery actions.
- Post-recovery validation.
- Lessons learned and preventive improvements.

## Safety

These exercises use synthetic data and must not interact
with real patient information or medical devices.