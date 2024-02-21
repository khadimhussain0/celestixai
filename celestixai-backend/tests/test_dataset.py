from fastapi.testclient import TestClient
from app import main as app

client = TestClient(app)


def test_upload_dataset():
    data = {"fname": "example.txt", "file": b"dummy file content"}

    response = client.post("/api/dataset/upload/", json=data)

    assert response.status_code == 201