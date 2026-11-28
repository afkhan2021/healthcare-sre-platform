# GitOps Deployment with Argo CD

## Overview

This project uses Argo CD to implement GitOps-based deployment
for the Healthcare SRE Platform development environment.

Argo CD continuously monitors the Git repository and compares
the desired Kubernetes state with the live cluster state.

## Application Configuration

- Application: healthcare-sre-platform-dev
- Repository: https://github.com/afkhan2021/healthcare-sre-platform
- Branch: main
- Manifest path: kubernetes/
- Namespace: healthcare-dev

## Synchronization Strategy

The Application enables automated synchronization with:

- Automated sync: applies approved changes committed to Git.
- Self-healing: reconciles live configuration drift against Git.
- Pruning: removes Kubernetes resources deleted from Git.

## Image Promotion

GitHub Actions builds and scans both container images.
After successful verification, the publishing workflow can
push images to Amazon ECR using immutable tags containing
the Git commit SHA and GitHub Actions run identifiers.

Image promotion is performed through a reviewed Git change
to the Kubernetes deployment configuration.

Argo CD then synchronizes the approved configuration.

## Security and Change Management

- Git is the source of truth for desired Kubernetes state.
- CI validates and scans application images and manifests.
- Image tags are immutable for traceability.
- Changes are reviewed before merging into main.
- Production promotion should use a separate environment
  with additional approval controls.

## Deployment Status

This repository contains the Argo CD Application definition.
A running Argo CD installation and Kubernetes cluster are
required before synchronization can occur.

No AWS infrastructure is provisioned by this configuration.