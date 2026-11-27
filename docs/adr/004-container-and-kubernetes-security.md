# ADR-004: Container and Kubernetes Workload Security

- **Status:** Accepted
- **Date:** 2026-11-27
- **Decision owners:** Platform Engineering and Security

## Context

The platform runs a synthetic healthcare API and incident automation service.

Containerized workloads must follow defense-in-depth principles and minimize the impact of a compromised application process or container.

## Decision

Adopt hardened container images and Kubernetes security contexts.

### Container controls

- Use a slim Python base image.
- Apply operating-system package updates during image builds.
- Upgrade pip and setuptools.
- Run application processes as a dedicated non-root user.
- Use Docker build context exclusions to avoid copying unnecessary files.
- Scan images for vulnerabilities using Trivy.

### Kubernetes controls

- Run workloads as non-root UID/GID 10001.
- Use a read-only root filesystem.
- Drop all Linux capabilities.
- Disable privilege escalation.
- Apply the RuntimeDefault seccomp profile.
- Disable automatic service-account token mounting.
- Apply a default-deny ingress network policy.

## Alternatives Considered

### Running containers as root

This simplifies file permissions but increases the potential impact of container compromise.

A dedicated non-root identity was selected to reduce privileges.

### Writable container root filesystem

A writable root filesystem provides convenience but increases the available locations for an attacker to modify.

A read-only root filesystem was selected for the Kubernetes workloads.

Applications requiring temporary writable storage must use explicitly defined writable volumes rather than making the entire root filesystem writable.

### Default-allow network policies

Default-allow networking simplifies initial connectivity but provides less workload isolation.

A default-deny ingress policy was selected as the starting point for restricting inbound pod traffic.

## Consequences

### Positive

- Reduced container privileges.
- Reduced writable filesystem exposure.
- More restrictive workload execution.
- Improved network isolation.
- Security controls are version-controlled and validated through CI.

### Trade-offs

- Read-only filesystems can require explicit writable temporary volumes.
- Network policies require careful review to avoid blocking legitimate traffic.
- Security contexts must be tested against application runtime requirements.

## Current Implementation Status

The API and incident receiver Kubernetes manifests include hardened security contexts.

The default-deny ingress network policy is implemented.

Trivy scanning of container images and Kubernetes manifests is integrated into GitHub Actions.

The optimized API image has been tested locally and confirmed to run as UID 10001.

## Review

Reassess workload permissions, filesystem requirements, network access, and vulnerability findings whenever application dependencies or deployment manifests change.
