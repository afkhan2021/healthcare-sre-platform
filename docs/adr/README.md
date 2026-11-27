# Architecture Decision Records

This directory documents the key architectural and engineering decisions behind the Healthcare SRE Platform.

Each ADR captures the context, decision, alternatives considered, consequences, and implementation status.

## Decision Index

| ADR | Decision | Description |
|---|---|---|
| [ADR-001](001-platform-architecture.md) | Platform Architecture | Cloud-native platform design and technology selection |
| [ADR-002](002-slo-and-error-budget-strategy.md) | SLO and Error-Budget Strategy | Reliability objectives, SLIs, error budgets, and burn-rate alerting |
| [ADR-003](003-secure-ci-cd-and-aws-identity.md) | Secure CI/CD and AWS Identity | GitHub Actions security, OIDC federation, and software supply-chain controls |
| [ADR-004](004-container-and-kubernetes-security.md) | Container and Kubernetes Security | Container hardening, Kubernetes security contexts, and network isolation |
| [ADR-005](005-infrastructure-and-cost-management.md) | Infrastructure and Cost Management | Terraform, environment separation, and AWS cost controls |

## ADR Status

All five records are currently marked **Accepted**.

## Adding New Decisions

Create a new numbered Markdown file using the naming convention:

`NNN-short-decision-title.md`

Include:

- Context
- Decision
- Alternatives Considered
- Consequences
- Current Implementation Status
- Review