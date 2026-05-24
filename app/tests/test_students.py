from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_students():
    response = client.get("/students")

    assert response.status_code == 200
