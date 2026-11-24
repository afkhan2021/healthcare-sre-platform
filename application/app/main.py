
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(
    title="Healthcare SRE Platform API",
    description="Synthetic healthcare patient services API",
    version="1.0.0"
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "healthcare_api_requests_total",
    "Total number of API requests"
)

# Synthetic patient records only
PATIENTS = [
    {
        "patient_id": "P1001",
        "name": "Alex Morgan",
        "status": "active"
    },
    {
        "patient_id": "P1002",
        "name": "Jordan Taylor",
        "status": "active"
    },
    {
        "patient_id": "P1003",
        "name": "Casey Lee",
        "status": "inactive"
    }
]


@app.get("/")
def root():
    REQUEST_COUNT.inc()
    return {
        "application": "Healthcare SRE Platform",
        "status": "running",
        "environment": "dev"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def readiness():
    return {"status": "ready"}


@app.get("/patients")
def get_patients():
    REQUEST_COUNT.inc()
    return {"patients": PATIENTS}


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    REQUEST_COUNT.inc()

    for patient in PATIENTS:
        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
