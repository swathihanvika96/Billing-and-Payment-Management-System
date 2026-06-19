from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_payments():

    response = client.get("/api/v1/payments")

    assert response.status_code in [200, 401, 403]