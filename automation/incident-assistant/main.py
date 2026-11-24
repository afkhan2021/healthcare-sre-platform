
from fastapi import FastAPI, Request
from datetime import datetime, timezone
from pathlib import Path

app = FastAPI(
    title="Healthcare SRE Incident Assistant",
    description="Classifies Grafana alerts and recommends incident runbooks",
    version="1.1.0"
)


APP_DIRECTORY = Path(__file__).resolve().parent

RUNBOOK_DIRECTORY = APP_DIRECTORY / "incidents" / "runbooks"

if not RUNBOOK_DIRECTORY.is_dir():
    PROJECT_ROOT = APP_DIRECTORY.parents[1]
    RUNBOOK_DIRECTORY = PROJECT_ROOT / "incidents" / "runbooks"


RUNBOOKS = {
    "HealthcareAPI_PodAvailability_Low": {
        "category": "Kubernetes Availability",
        "severity": "warning",
        "runbook": "pod-availability-low.md",
        "investigation_steps": [
            {
                "step": "Check deployment replica availability",
                "command": "kubectl get deployment healthcare-api -n healthcare-dev"
            },
            {
                "step": "Inspect Healthcare API pods",
                "command": "kubectl get pods -n healthcare-dev -l app=healthcare-api -o wide"
            },
            {
                "step": "Review recent Kubernetes events",
                "command": "kubectl get events -n healthcare-dev --sort-by=.lastTimestamp"
            },
            {
                "step": "Inspect application logs",
                "command": "kubectl logs deployment/healthcare-api -n healthcare-dev --tail=100"
            },
            {
                "step": "Check node health",
                "command": "kubectl get nodes"
            }
        ],
        "potential_causes": [
            {
                "cause": "Memory limit exceeded",
                "symptom": "Container terminated with OOMKilled",
                "diagnostic_command": "kubectl describe pods -n healthcare-dev -l app=healthcare-api"
            },
            {
                "cause": "Application crash",
                "symptom": "Pod enters CrashLoopBackOff",
                "diagnostic_command": "kubectl logs deployment/healthcare-api -n healthcare-dev --tail=100"
            },
            {
                "cause": "Container image pull failure",
                "symptom": "Pod enters ImagePullBackOff",
                "diagnostic_command": "kubectl describe pods -n healthcare-dev -l app=healthcare-api"
            },
            {
                "cause": "Insufficient cluster resources",
                "symptom": "Pod remains Pending",
                "diagnostic_command": "kubectl describe nodes"
            },
            {
                "cause": "Kubernetes node health issue",
                "symptom": "Node reports NotReady or resource pressure",
                "diagnostic_command": "kubectl get nodes"
            }
        ],
        "recommended_remediation": [
            {
                "action": "Restore the expected replica count",
                "description": "If a replica is unavailable and the deployment is healthy enough to recover, restore the desired replica count to two.",
                "command": "kubectl scale deployment healthcare-api --replicas=2 -n healthcare-dev",
                "approval_required": True
            },
            {
                "action": "Investigate unhealthy pods",
                "description": "Inspect pod status, events, and previous container logs before restarting or replacing workloads.",
                "command": "kubectl describe pods -n healthcare-dev -l app=healthcare-api",
                "approval_required": True
            },
            {
                "action": "Verify service recovery",
                "description": "Confirm both replicas are available and ready before closing the incident.",
                "command": "kubectl get deployment healthcare-api -n healthcare-dev",
                "approval_required": False
            }
        ]
    }
}

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/webhook")
async def receive_alert(request: Request):
    payload = await request.json()

    incidents = []

    for alert in payload.get("alerts", []):
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        alert_name = labels.get("alertname", "unknown")
        classification = RUNBOOKS.get(alert_name, {})

        runbook_name = classification.get("runbook")
        runbook_path = RUNBOOK_DIRECTORY / runbook_name if runbook_name else None

        runbook_available = (
            runbook_path is not None and runbook_path.is_file()
        )

        incidents.append({
            "alert_name": alert_name,
            "status": payload.get("status", "unknown"),
            "severity": classification.get(
                "severity",
                labels.get("severity", "unknown")
            ),
            "category": classification.get("category", "Unclassified"),
            "summary": annotations.get("summary", ""),
            "description": annotations.get("description", ""),
            "runbook": runbook_name,
            "runbook_available": runbook_available,
            "investigation_steps": classification.get(
                "investigation_steps", []
            ),
            "potential_causes": classification.get(
                "potential_causes", []
            ),
            "recommended_remediation": classification.get(
                "recommended_remediation", []
            )

        })

    event = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "incident_count": len(incidents),
        "incidents": incidents
    }

    print("INCIDENT ASSISTANT EVENT:")
    print(event)

    return event
