
# Exercise 03: Failed Deployment and Rollback

## Objective

Simulate an unsuccessful application deployment, identify rollout failures, restore the previous healthy release, and validate service recovery.

Skills demonstrated:

- Kubernetes rolling deployments.
- Deployment rollout monitoring.
- Failed release investigation.
- Rollback and release recovery.
- Deployment safety and change management.

## 1. Scenario

A new Healthcare API release is deployed to the development environment.

The new container image cannot start successfully. Kubernetes reports unavailable replicas and the rollout does not complete.

The SRE team must identify the failed release, restore the previous healthy revision, and verify application availability.

## 2. Safety and Environment

- Use only an isolated local or development Kubernetes cluster.
- The `healthcare-dev` namespace must contain only disposable exercise workloads.
- Never execute against production or shared workloads.
- Use synthetic application data only.
- The previous AWS EKS cluster has been destroyed.
- This exercise is documented for future execution.

## 3. Baseline Verification

Confirm the current deployment and image:

    kubectl get deployment healthcare-api -n healthcare-dev
    kubectl get pods -n healthcare-dev
    kubectl describe deployment healthcare-api -n healthcare-dev

Record the currently deployed image and available replica count.

## 4. Failure Injection

Deploy an intentionally invalid image tag:

    kubectl set image deployment/healthcare-api \
      healthcare-api=busybox:invalid-tag \
      -n healthcare-dev

Observe the rollout:

    kubectl rollout status deployment/healthcare-api -n healthcare-dev --timeout=90s

The command may time out because the new replica cannot become Ready. This is expected during the simulated failure.

Inspect the deployment and pod events:

    kubectl get pods -n healthcare-dev
    kubectl describe deployment healthcare-api -n healthcare-dev
    kubectl get events -n healthcare-dev --sort-by='.lastTimestamp'

Expected symptoms:

- ImagePullBackOff or ErrImagePull.
- New replicas fail to become Ready.
- Deployment rollout does not complete.
- Existing healthy replicas may continue serving traffic depending on rolling-update settings.

## 5. Investigation

Inspect rollout history:

    kubectl rollout history deployment/healthcare-api -n healthcare-dev

Identify the failed revision and compare it with the previous known-good revision.

Check pod events and image details to confirm the invalid image reference.

Expected root cause: the deployment references an image tag that does not exist or cannot be pulled.

## 6. Recovery

Roll back to the previous deployment revision:

    kubectl rollout undo deployment/healthcare-api -n healthcare-dev

Monitor recovery:

    kubectl rollout status deployment/healthcare-api -n healthcare-dev --timeout=90s

Verify the deployment and pods:

    kubectl get deployment healthcare-api -n healthcare-dev
    kubectl get pods -n healthcare-dev

Confirm the restored image:

    kubectl get deployment healthcare-api -n healthcare-dev \
      -o jsonpath='{.spec.template.spec.containers[0].image}'

## 7. Recovery Validation

Confirm:

- Deployment rollout completes successfully.
- Expected replicas are available.
- Pods are Running and Ready.
- The previous known-good image is restored.
- Application health and readiness checks succeed.
- Availability and error-rate SLIs return to acceptable levels.
- Relevant alerts return to Normal.

## 8. Preventive Improvements

- Validate image references before deployment.
- Use immutable image tags or digests.
- Require CI security and test checks before release.
- Apply deployment health checks and rollout monitoring.
- Define rollback procedures and release ownership.
- Use progressive delivery for high-risk changes where appropriate.

## 9. Lessons Learned

Document:

- Failed release and deployment revision.
- Detection method and time to detect.
- Root cause and contributing factors.
- Rollback duration and recovery evidence.
- Customer or service impact.
- Improvements to release safeguards.

## 10. Exercise Status

**Documented; execution pending.**

A disposable Kubernetes environment with a working baseline deployment is required to execute this exercise.

No live deployment failure or rollback is claimed.
