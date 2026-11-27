# ADR-003: Secure CI/CD and AWS Workload Identity

- **Status:** Accepted
- **Date:** 2026-11-27
- **Decision owners:** Platform Engineering and Security

## Context

The platform requires automated testing, security validation, software supply-chain visibility, and an eventual path to publishing container images to Amazon ECR.

CI/CD must avoid unnecessary long-lived credentials and restrict deployment permissions.

## Decision

Use GitHub Actions for continuous integration and security validation.

Use GitHub Actions OpenID Connect (OIDC) federation as the intended authentication mechanism for AWS operations.

The Terraform configuration defines:

- An AWS IAM OIDC identity provider.
- A dedicated GitHub Actions IAM role.
- A trust policy restricted to the project's GitHub repository and main branch.
- ECR publishing permissions scoped to the project's repositories.

Container publishing is gated until the required AWS configuration is explicitly provided.

## Security Controls

The CI pipeline includes:

- Automated Python tests.
- Minimum code coverage enforcement.
- Bandit static application security analysis.
- pip-audit dependency vulnerability checks.
- Trivy container image scanning.
- Critical vulnerability gates.
- Kubernetes manifest security scanning.
- CycloneDX SBOM generation.

Container images use non-root application identities and hardened runtime configurations.

## Alternatives Considered

### Long-lived AWS access keys

**Advantages:**
- Simple initial setup.
- Widely supported by automation tools.

**Disadvantages:**
- Credentials require secure storage and rotation.
- Leaked credentials can remain valid until revoked or expired.
- Greater long-term credential-management overhead.

### GitHub Actions OIDC federation

**Advantages:**
- Avoids storing long-lived AWS access keys.
- Uses short-lived role credentials.
- Allows trust policies to restrict repository and branch identity.
- Supports least-privilege IAM permissions.

**Trade-offs:**
- Requires OIDC provider and IAM trust configuration.
- Trust policies must be carefully scoped and maintained.

OIDC was selected for the AWS authentication design.

## Consequences

### Positive

- Reduced long-lived credential exposure.
- Repository-scoped AWS role assumption.
- Restricted ECR publishing permissions.
- Automated security checks integrated into CI.
- SBOM artifacts provide software component visibility.

### Trade-offs

- CI configuration and IAM policies require maintenance.
- Vulnerability findings require triage and remediation.
- Security scanning does not guarantee that an image is vulnerability-free.

## Cost and Deployment Controls

AWS image publishing remains disabled until AWS role and region configuration is explicitly supplied.

The project can continue running local builds and GitHub Actions validation without provisioning AWS infrastructure.

## Current Implementation Status

The GitHub Actions CI and security workflow is implemented and has passed successful workflow runs.

Terraform definitions for GitHub OIDC and ECR are implemented and validated.

AWS resources have not been provisioned, and image publishing has not been enabled.

## Review

Review IAM permissions, repository trust conditions, scanning policies, and deployment gates whenever the CI/CD architecture changes.
