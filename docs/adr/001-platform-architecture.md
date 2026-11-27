# ADR-001: Healthcare SRE Platform Architecture

- **Status:** Accepted
- **Date:** 2026-11-27
- **Decision owners:** Platform Engineering

## Context

The project requires a production-inspired platform that demonstrates enterprise SRE practices for a synthetic healthcare application.

The architecture must support:

- Measurable reliability objectives.
- Kubernetes-based application orchestration.
- Infrastructure as Code.
- Automated testing and security validation.
- Centralized observability.
- Incident detection and operational response.
- Secure software delivery.
- Cost-conscious development and deployment.

The platform must remain an independent educational project and must not interact with medical devices or real patient data.

## Decision

Adopt a cloud-native architecture based on the following components:

| Layer | Technology | Responsibility |
|---|---|---|
| Application | Python and FastAPI | Synthetic healthcare API |
| Containerization | Docker | Portable application packaging |
| Orchestration | Kubernetes and Amazon EKS | Workload scheduling and management |
| Infrastructure | Terraform | Reproducible infrastructure definitions |
| CI/CD | GitHub Actions | Automated validation and security gates |
| Observability | Prometheus and Grafana | Metrics, SLI monitoring, and visualization |
| Security | Bandit, pip-audit, and Trivy | Application, dependency, and container security |
| Incident response | Python automation and runbooks | Alert classification and remediation recommendations |

The architecture separates application, infrastructure, monitoring, security, and incident automation responsibilities.

## Alternatives Considered

### 1. Virtual machines instead of Kubernetes

**Advantages:**
- Simpler initial deployment.
- Lower orchestration complexity.

**Disadvantages:**
- Less opportunity to demonstrate container orchestration.
- More manual workload management.
- Less representative of the Kubernetes platform engineering practices targeted by this project.

### 2. Managed Kubernetes instead of self-managed Kubernetes

Amazon EKS was selected as the intended managed Kubernetes platform.

**Advantages:**
- Managed control plane.
- Integration with AWS identity and networking services.
- Demonstrates cloud-native platform engineering.

**Trade-offs:**
- Additional service costs.
- Operational complexity across networking, IAM, compute, and cluster components.

### 3. Manual infrastructure provisioning instead of Terraform

Terraform was selected to make infrastructure definitions repeatable, reviewable, and version controlled.

## Consequences

### Positive

- Clear separation of engineering responsibilities.
- Repeatable infrastructure definitions.
- Automated quality and security checks.
- Measurable service reliability.
- A platform suitable for demonstrating enterprise SRE practices.

### Trade-offs

- Kubernetes and EKS introduce operational and financial complexity.
- Observability components require resource planning.
- Secure automation requires careful identity and permission design.
- The architecture must be operated within an explicit cost budget.

## Cost Management

AWS infrastructure is intentionally not provisioned during normal local development.

The project uses local Docker builds and GitHub Actions validation to demonstrate substantial engineering capabilities without maintaining an active EKS environment.

AWS deployment is deferred until explicitly required.

## Current Implementation Status

The application, Kubernetes manifests, Terraform modules, monitoring definitions, security controls, incident automation, and CI workflow are implemented.

The AWS environment is not currently deployed. The architecture describes the intended cloud deployment rather than claiming an active production environment.

## Review

Revisit this decision if deployment requirements, reliability objectives, operational complexity, or cost constraints change.
