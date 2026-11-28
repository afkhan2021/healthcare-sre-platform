# Healthcare SRE Platform

**By Arif Faheem Khan**

A production-inspired, cloud-native Healthcare Site Reliability Engineering platform demonstrating reliability engineering, Kubernetes operations, infrastructure as code, observability, security automation, and incident response.

> **Portfolio project:** This is an independent project using synthetic healthcare data. It is not affiliated with Tandem Diabetes Care, is not a certified medical platform, and does not interact with or control medical devices.

## Project Overview

The Healthcare SRE Platform demonstrates how to build, secure, monitor, and operate a cloud-native application platform using modern Site Reliability Engineering practices.

The platform includes:

- A FastAPI application with synthetic patient records.
- Kubernetes deployment configurations.
- Terraform infrastructure modules.
- Prometheus metrics, SLIs, SLOs, and alerting.
- Grafana observability.
- Automated incident classification and remediation recommendations.
- CI/CD security scanning and software supply chain controls.
- GitOps configuration using Argo CD.
- Disaster recovery documentation and incident exercises.

The project emphasizes operational readiness, reliability, security, automation, and engineering trade-offs relevant to enterprise environments.

## Architecture and Technology

| Area | Technologies |
|---|---|
| Application | Python, FastAPI, Uvicorn |
| Containerization | Docker |
| Orchestration | Kubernetes, Amazon EKS, Helm |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| CI/CD | GitHub Actions |
| GitOps | Argo CD, Kustomize |
| Observability | Prometheus, Grafana |
| Metrics | Prometheus client, custom application metrics |
| Security | Bandit, pip-audit, Trivy |
| Software Supply Chain | CycloneDX SBOM |
| Automation | Python, Bash, Terraform |
| Incident Management | Alert classification, runbooks, remediation recommendations |

## Reliability Engineering

The platform defines measurable service-level objectives and supporting observability.

### Service-level objectives

| Indicator | Objective |
|---|---|
| Availability | 99.9% |
| HTTP 5xx error rate | At most 0.1% |
| Latency | At least 95% of eligible requests within 300 ms |

A 99.9% availability objective has a time-based equivalent of approximately 43.8 minutes over a 30-day month.

The platform's availability SLI is request-based, however, so actual error-budget consumption is calculated from eligible requests rather than downtime minutes.

Implemented capabilities:

- Custom application metrics.
- Prometheus SLI recording rules.
- Availability, error-rate, and latency measurements.
- Multi-window error-budget burn-rate alerts.
- SLO breach alerting.
- Grafana SLI visualization.

## Application

The FastAPI service exposes:

| Endpoint | Purpose |
|---|---|
| `/` | Application information |
| `/health` | Health check |
| `/ready` | Readiness check |
| `/patients` | Synthetic patient records |
| `/patients/{id}` | Retrieve a synthetic patient |
| `/metrics` | Prometheus metrics |

All patient records are synthetic and intended exclusively for demonstration.

## Incident Management Automation

The Python incident receiver demonstrates how alert events can be classified and mapped to operational runbooks.

Capabilities include:

- Alert classification.
- Runbook mapping.
- Remediation recommendations.
- Approval-required remediation workflows.

For example, a low API pod availability alert maps to a corresponding runbook and recommends restoring the API deployment to two replicas.

The remediation recommendation requires approval rather than automatically executing an unapproved production change.

## Container and Kubernetes Security

Security controls are integrated into the application, container configuration, Kubernetes manifests, and CI pipeline.

Implemented controls include:

- Non-root container execution.
- Dedicated application user (UID 10001).
- Read-only container root filesystem.
- Dropped Linux capabilities.
- RuntimeDefault seccomp profile.
- Disabled automatic service-account token mounting.
- Kubernetes default-deny ingress network policy.
- Python dependency vulnerability auditing.
- Static application security analysis.
- Container image vulnerability scanning.
- Kubernetes manifest security scanning.
- CycloneDX software bill of materials generation.

The CI workflow generates SBOM artifacts for both application containers.

## CI/CD and Quality Gates

GitHub Actions automates validation and security checks on repository changes.

The pipeline includes:

1. Python unit tests.
2. Code coverage enforcement (90% minimum).
3. Bandit static security analysis.
4. pip-audit dependency vulnerability checks.
5. API and incident receiver container builds.
6. Trivy container vulnerability scanning.
7. Critical vulnerability gates.
8. Kubernetes manifest security scanning.
9. CycloneDX SBOM generation and artifact upload.

Container publishing to Amazon ECR is configured through GitHub Actions OpenID Connect (OIDC). Publishing is gated behind explicit AWS configuration.

## GitOps

The repository includes an Argo CD Application definition configured to:

- Monitor the GitHub repository's `main` branch.
- Use the Kubernetes manifests under `kubernetes/`.
- Reconcile the development namespace.
- Support automated synchronization, pruning, and self-healing.

Argo CD installation and a running Kubernetes cluster are required for live GitOps reconciliation. The configuration is documented; live reconciliation is not currently claimed.

## Disaster Recovery and Incident Exercises

The project includes operational documentation covering:

- Disaster recovery and business continuity.
- Kubernetes pod availability incidents.
- CrashLoopBackOff troubleshooting.
- Healthcare API outage and SLO burn.
- Failed deployment and rollback.

The three incident simulation exercises are documented for future execution in an isolated Kubernetes environment. They are not represented as completed live simulations.

## Local Development

### Prerequisites

- Python 3.12
- Git
- Optional: Docker for container builds

No AWS account or running Kubernetes cluster is required to run the API and its tests locally.

### 1. Clone the repository

```bash
git clone https://github.com/afkhan2021/healthcare-sre-platform.git
cd healthcare-sre-platform
```

### 2. Create and activate a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r application/requirements.txt
python -m pip install -r application/requirements-dev.txt
```

### 4. Run the application

```bash
PYTHONPATH=application python -m uvicorn app.main:app --reload
```

Open:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Metrics: http://127.0.0.1:8000/metrics

### 5. Run tests

In a separate terminal, activate the virtual environment and run:

```bash
PYTHONPATH=application python -m pytest application/tests/test_main.py \
  --cov=app.main \
  --cov-report=term-missing \
  --cov-fail-under=90 \
  -v
```

### 6. Build the API container

From the repository root:

```bash
docker build -f application/Dockerfile -t healthcare-sre-api:local .
```

## Project Documentation

### Architecture and design decisions

- [Architecture Decision Records](docs/adr/README.md)
- [Platform Architecture](docs/adr/001-platform-architecture.md)
- [SLO and Error-Budget Strategy](docs/adr/002-slo-and-error-budget-strategy.md)
- [Secure CI/CD and AWS Identity](docs/adr/003-secure-ci-cd-and-aws-identity.md)
- [Container and Kubernetes Security](docs/adr/004-container-and-kubernetes-security.md)
- [Infrastructure and Cost Management](docs/adr/005-infrastructure-and-cost-management.md)

### Operations and reliability

- [Runbooks Index](docs/runbooks/README.md)
- [Pod Availability Low Runbook](incidents/runbooks/pod-availability-low.md)
- [Incident Postmortem](incidents/postmortems/2026-11-24-pod-availability-incident.md)
- [Disaster Recovery Plan](docs/dr/disaster-recovery-plan.md)
- [Incident Simulation Exercises](incidents/exercises/README.md)

### Security and delivery

- [Container Security Assessment](security/container-security-assessment.md)
- [Container SBOM](security/container-sbom.cdx)
- [Argo CD GitOps Configuration](argocd/README.md)
- [GitHub Actions CI Workflow](.github/workflows/ci.yml)

## Infrastructure and Cost Management

The project is designed with cost-conscious development practices:

- AWS infrastructure is not currently provisioned.
- EKS and associated compute resources are deferred until deployment is explicitly required.
- Container publishing is gated behind explicit AWS configuration.
- ECR lifecycle policies retain the two most recently pushed tagged images per repository.
- Local development and GitHub Actions validation support development without running AWS infrastructure.

The previous development EKS environment was destroyed after testing. No AWS infrastructure is currently deployed.

## Project Scope and Limitations

This repository demonstrates architecture, implementation, automation, and operational documentation. It does not claim production certification or continuous live operation.

- Kubernetes and observability components were tested in the previous development environment.
- The current repository includes Kubernetes and Argo CD configuration, but no live cluster is running.
- The three incident exercises are documented; live execution is pending.
- The disaster recovery objectives are proposed targets, not measured recovery guarantees.
- All patient information is synthetic.

## Author

**Arif Faheem Khan**

Lead Site Reliability Engineer | DevOps | Platform Engineering | Cloud & AI

GitHub: [@afkhan2021](https://github.com/afkhan2021)

Repository: [healthcare-sre-platform](https://github.com/afkhan2021/healthcare-sre-platform)
