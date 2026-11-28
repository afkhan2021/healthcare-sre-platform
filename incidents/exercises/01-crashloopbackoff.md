
# Exercise 01: Kubernetes CrashLoopBackOff

## Objective

Simulate a container startup failure, investigate Kubernetes restart behavior, and recover the workload.

## Safety

- Use only an isolated development or local Kubernetes cluster.
- Use the disposable namespace `incident-lab`.
- Never run against production or shared workloads.
- Execution is pending because the previous AWS EKS cluster was destroyed.

## 1. Failure Injection

Create the namespace:

    kubectl create namespace incident-lab

Create a deployment with an intentionally failing command:

    kubectl create deployment crashloop-demo \
      --namespace incident-lab \
      --image=busybox:1.36 \
      -- /bin/sh -c 'exit 1'

Observe the pod:

    kubectl get pods -n incident-lab -w

Expected: repeated container restarts followed by CrashLoopBackOff.

## 2. Investigation

    kubectl describe pods -n incident-lab
    kubectl logs deployment/crashloop-demo -n incident-lab
    kubectl logs deployment/crashloop-demo -n incident-lab --previous
    kubectl get events -n incident-lab --sort-by='.lastTimestamp'

Expected root cause: the startup command exits immediately with status code 1.

## 3. Recovery

Replace the failing command:

    kubectl patch deployment crashloop-demo \
      -n incident-lab \
      --type='json' \
      -p='[{"op":"replace","path":"/spec/template/spec/containers/0/command","value":["/bin/sh","-c","sleep 3600"]}]'

Verify recovery:

    kubectl rollout status deployment/crashloop-demo -n incident-lab
    kubectl get deployment,pods -n incident-lab

Expected: one available replica and a Running pod.

## 4. Preventive Improvements

- Validate container startup commands in CI.
- Use appropriate startup and readiness probes.
- Monitor container restart counts.
- Investigate exit codes and previous container logs.
- Apply resource requests and limits.

## 5. Cleanup

    kubectl delete namespace incident-lab

## Exercise Status

**Documented; execution pending.**

A local or development Kubernetes cluster is required to execute this exercise. No live execution has been claimed.
