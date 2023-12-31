from http.client import OK

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == OK
