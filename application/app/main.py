
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = FastAPI(
    title="Healthcare SRE Platform API",
    description="Synthetic healthcare patient services API",
    version="2.0.0",
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "healthcare_api_requests",
    "Total HTTP requests received",
    ["method", "endpoint"],
)

REQUESTS_BY_STATUS = Counter(
    "healthcare_api_requests_by_status",
    "Total HTTP requests grouped by status code",
    ["status_code"],
)

ERROR_COUNT = Counter(
    "healthcare_api_errors",
    "Total HTTP 5xx server errors",
    ["status_code"],
)

REQUEST_DURATION = Histogram(
    "healthcare_api_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.3, 0.5, 1, 2.5, 5, 10),
)


@app.middleware("http")
async def prometheus_metrics_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        # Avoid counting Prometheus scrapes as application traffic.
        if request.url.path not in ("/metrics", "/health", "/ready"):
            duration = time.perf_counter() - start_time

            route = request.scope.get("route")
            endpoint = getattr(route, "path", "unmatched")

            method = request.method

            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
            ).inc()

            REQUESTS_BY_STATUS.labels(
                status_code=str(status_code),
            ).inc()

            if status_code >= 500:
                ERROR_COUNT.labels(
                    status_code=str(status_code),
                ).inc()

            # Exclude HTTP 4xx responses from latency measurements.
            if status_code < 400:
                REQUEST_DURATION.labels(
                    method=method,
                    endpoint=endpoint,
                ).observe(duration)

# Synthetic patient records only
PATIENTS = [
    {
        "patient_id": "P1001",
        "name": "Alex Morgan",
        "status": "active",
    },
    {
        "patient_id": "P1002",
        "name": "Jordan Taylor",
        "status": "active",
    },
    {
        "patient_id": "P1003",
        "name": "Casey Lee",
        "status": "inactive",
    },
]


@app.get("/")
def root():
    return {
        "application": "Healthcare SRE Platform",
        "status": "running",
        "environment": "dev",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def readiness():
    return {"status": "ready"}


@app.get("/patients")
def get_patients():
    return {"patients": PATIENTS}


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    for patient in PATIENTS:
        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found",
    )


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
