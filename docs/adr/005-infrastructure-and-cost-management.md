# ADR-005: Infrastructure as Code and Cloud Cost Management

- **Status:** Accepted
- **Date:** 2026-11-27
- **Decision owners:** Platform Engineering

## Context

The platform needs reproducible cloud infrastructure while keeping development and demonstration costs low.

The infrastructure design must support secure AWS integration without requiring continuously running cloud resources.

## Decision

Use Terraform to define and manage AWS infrastructure.

Organize infrastructure into reusable modules and separate environment configurations.

The current Terraform design includes:

- Amazon ECR repositories for application images.
- GitHub Actions OIDC identity federation.
- A dedicated IAM role for CI image publishing.
- Repository-scoped ECR permissions.
- ECR lifecycle policies to limit retained tagged images.

## Environment Strategy

Keep registry infrastructure separate from the application development environment.

AWS infrastructure is not provisioned during normal local development.

Terraform configuration can be validated locally without creating cloud resources.

Any future AWS deployment requires an explicit cost review and approval.

## Cost Management

Prioritize local development and GitHub Actions validation.

Defer resources with ongoing or potentially significant costs, including:

- Amazon EKS clusters.
- EC2 worker nodes.
- NAT Gateways.
- Application Load Balancers.
- Persistent cloud monitoring infrastructure.

Avoid leaving demonstration environments running when they are not required.

Use ECR lifecycle policies to limit the number of retained tagged container images.

## Alternatives Considered

### Always-on AWS environment

An always-on environment provides continuous cloud availability but introduces recurring costs even when the platform is not being demonstrated.

This option was deferred in favor of cost-conscious deployment.

### Manual AWS configuration

Manual provisioning can be quick for initial experiments but is difficult to reproduce, review, and maintain.

Terraform was selected to provide version-controlled infrastructure definitions.

## Consequences

### Positive

- Reproducible infrastructure definitions.
- Reusable Terraform modules.
- Separation of infrastructure environments.
- Reduced risk of unnecessary cloud spending.
- A clear path to future AWS deployment.

### Trade-offs

- Cloud deployment demonstrations require deliberate provisioning.
- Infrastructure changes require Terraform review and validation.
- Deferred AWS deployment means cloud integration is not currently demonstrated as an active environment.

## Current Implementation Status

Terraform modules for ECR and GitHub Actions OIDC are implemented and validated.

The GitHub Actions workflow includes a conditional image-publishing job that remains disabled until the required AWS configuration is supplied.

No AWS infrastructure is currently deployed for this project.

## Review

Reassess infrastructure requirements, deployment frequency, and estimated monthly costs before provisioning or expanding AWS resources.
