
from fastapi.testclient import TestClient
from fastapi.responses import Response

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_endpoint():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_get_patients():
    response = client.get("/patients")

    assert response.status_code == 200

    patients = response.json()["patients"]

    assert len(patients) == 3
    assert all("patient_id" in patient for patient in patients)


def test_get_existing_patient():
    response = client.get("/patients/P1001")

    assert response.status_code == 200
    assert response.json()["patient_id"] == "P1001"


def test_get_nonexistent_patient():
    response = client.get("/patients/P9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_prometheus_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "healthcare_api_requests" in response.text
    assert "healthcare_api_errors" in response.text
    assert "healthcare_api_request_duration_seconds" in response.text


def test_server_error_increments_error_metric():
    def simulated_server_error():
        return Response(status_code=500)

    app.add_api_route(
        "/test-server-error",
        simulated_server_error,
        methods=["GET"],
    )

    test_client = TestClient(app)

    response = test_client.get("/test-server-error")

    assert response.status_code == 500

    metrics_response = test_client.get("/metrics")

    assert 'healthcare_api_errors_total{status_code="500"}' in metrics_response.text
