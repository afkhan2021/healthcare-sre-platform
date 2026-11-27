# ADR-002: Service-Level Objectives and Error-Budget Strategy

- **Status:** Accepted
- **Date:** 2026-11-27
- **Decision owners:** Site Reliability Engineering

## Context

The platform needs measurable reliability targets rather than relying exclusively on infrastructure health or subjective assessments of service quality.

The application must expose meaningful SLIs that represent user-facing service behavior.

## Decision

Adopt an SLO-based reliability model using Prometheus metrics, recording rules, alert rules, and Grafana dashboards.

The initial objectives are:

| SLI | SLO |
|---|---|
| Availability | 99.9% |
| HTTP 5xx error rate | At most 0.1% |
| Request latency | 95% of eligible requests within 300 ms |

The availability objective allows approximately 43.8 minutes of unavailability in a 30-day month.

## Measurement Strategy

The application exposes custom Prometheus metrics for:

- Total API requests.
- Requests grouped by HTTP status.
- Server-side errors.
- Request duration.

Prometheus recording rules calculate availability, error rate, and latency compliance.

Client-side 4xx responses are excluded from the eligible server-error calculation because they generally represent invalid client requests rather than service failures.

## Alerting Strategy

Prometheus alert rules monitor SLO compliance and error-budget consumption.

The implementation includes:

- SLO breach alerts.
- Multi-window, multi-burn-rate alerting.
- Error-budget monitoring.
- API pod availability alerts.

The intent is to detect both sustained reliability degradation and rapid error-budget consumption.

## Alternatives Considered

### Infrastructure-only monitoring

Monitoring CPU, memory, and pod health is useful but does not establish whether users are receiving a reliable service.

### Static threshold alerting

Simple thresholds are easy to implement but can generate noise and fail to represent the impact of an incident on the error budget.

An SLO-based approach provides a more meaningful measure of service reliability.

## Consequences

### Positive

- Reliability is measured using service behavior.
- Error budgets make reliability trade-offs explicit.
- Burn-rate alerts help prioritize incidents based on their impact.
- Engineering teams gain measurable reliability targets.

### Trade-offs

- SLOs require meaningful traffic and carefully defined measurement windows.
- Low traffic can make short-window measurements noisy.
- Recording rules and alert thresholds require ongoing review.

## Operational Principle

Reliability targets should guide engineering priorities.

When error-budget consumption becomes excessive, the team should prioritize reliability improvements over introducing additional changes that increase operational risk.

## Current Implementation Status

Prometheus SLI recording rules, SLO alert rules, custom application metrics, and Grafana SLI visualization are implemented.

The objectives are portfolio-project targets and have not been validated against a live production healthcare workload.

## Review

Revisit the objectives as traffic patterns, service requirements, and operational evidence evolve.
