# Healthcare SRE Platform

### By Arif Faheem Khan

A production-inspired, cloud-native Healthcare Site Reliability Engineering platform demonstrating reliability engineering, Kubernetes operations, infrastructure as code, observability, security automation, and incident response.

> This is an independent portfolio project using synthetic healthcare data. It is not affiliated with Tandem Diabetes Care, is not a certified medical platform, and does not interact with or control medical devices.

## Project Overview

The Healthcare SRE Platform demonstrates how to build and operate a secure, observable, and resilient application platform using modern SRE practices.

The application exposes synthetic patient information through a FastAPI service. The platform includes automated testing, service-level indicators, service-level objectives, error-budget monitoring, incident alerting, container security controls, and infrastructure automation.

The project is designed to demonstrate engineering decisions and operational practices relevant to enterprise and regulated environments.

## Architecture and Technology

| Area | Technologies |
|---|---|
| Application | Python, FastAPI, Uvicorn |
| Containerization | Docker |
| Orchestration | Kubernetes, Amazon EKS, Helm |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| CI/CD | GitHub Actions |
| Observability | Prometheus, Grafana |
| Metrics | Prometheus client, custom application metrics |
| Security | Bandit, pip-audit, Trivy |
| Software Supply Chain | CycloneDX SBOM |
| Automation | Python, Bash, Terraform |
| Incident Management | Alert classification, runbooks, remediation recommendations |

## Reliability Engineering

The project implements measurable service-level objectives and supporting observability.

### Service-level objectives

| Indicator | Objective |
|---|---|
| Availability | 99.9% |
| HTTP 5xx error rate | At most 0.1% |
| Latency | 95% of eligible requests within 300 ms |

The 99.9% monthly availability objective corresponds to approximately 43.8 minutes of error budget in a 30-day month.

Implemented reliability capabilities include:

- Custom application metrics.
- Prometheus SLI recording rules.
- Availability, error-rate, and latency measurements.
- SLO breach and multi-window burn-rate alerts.
- Error-budget monitoring.
- Grafana SLI visualization.

## Application Endpoints

The FastAPI service exposes:

| Endpoint | Purpose |
|---|---|
| `/` | Application information |
| `/health` | Liveness/health check |
| `/ready` | Readiness check |
| `/patients` | Synthetic patient records |
| `/patients/{id}` | Retrieve a synthetic patient |
| `/metrics` | Prometheus metrics |

All patient records are synthetic and intended only for demonstration.

## Incident Management Automation

The incident automation component demonstrates how alert events can be classified and connected to operational runbooks.

Implemented capabilities include:

- Alert classification.
- Runbook mapping.
- Remediation recommendations.
- Approval-required remediation workflows.

For example, a low API pod availability alert maps to a runbook and recommends restoring the API deployment to two replicas. The remediation recommendation requires approval rather than executing an unapproved production change.

## Container and Kubernetes Security

Security is integrated into the application and CI pipeline.

Implemented controls include:

- Non-root container execution.
- Dedicated application user (UID 10001).
- Read-only container root filesystem in Kubernetes.
- Dropped Linux capabilities.
- RuntimeDefault seccomp profile.
- Disabled automatic service-account token mounting.
- Kubernetes default-deny ingress network policy.
- Python dependency vulnerability auditing.
- Static application security analysis.
- Container image vulnerability scanning.
- Kubernetes manifest security scanning.
- CycloneDX software bill of materials generation.

The GitHub Actions workflow generates SBOM artifacts for both application containers.

## CI/CD and Quality Gates

GitHub Actions automates the project's validation and security checks.

The pipeline includes:

1. Python test execution.
2. Code coverage enforcement (90% minimum).
3. Bandit security analysis.
4. Python dependency auditing with pip-audit.
5. Container image builds.
6. Trivy container vulnerability scanning.
7. Critical vulnerability gates.
8. Kubernetes manifest security scanning.
9. CycloneDX SBOM generation.

Container publishing to Amazon ECR is configured through GitHub Actions OIDC. Publishing remains disabled until AWS configuration is explicitly provided.

## Infrastructure and Cost Management

The project is designed with cost-conscious deployment practices:

- AWS infrastructure is intentionally not provisioned during local development.
- EKS and associated compute resources are deferred until deployment is explicitly required.
- Container publishing is gated behind explicit AWS configuration.
- ECR lifecycle policies retain the two most recently pushed tagged images per repository.
- Local Docker builds and GitHub Actions validation allow development without provisioning AWS resources.

No AWS infrastructure is currently deployed. The application and its tests can run locally without AWS resources.