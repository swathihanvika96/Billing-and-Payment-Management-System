from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_customers():

    response = client.get("/api/v1/customers")

    assert response.status_code in [200, 401, 403]