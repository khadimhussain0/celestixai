from fastapi.testclient import TestClient
from app import main as app

client = TestClient(app)


def test_upload_dataset():
    data = {"fname": "example.txt", "file": b"dummy file content"}

    response = client.post("/api/dataset/upload/", json=data)

    assert response.status_code == 201

    # Optionally, you can assert the response content or structure
    # For example, if your route returns JSON, you can assert the JSON content
    # assert response.json() == {"message": "Dataset uploaded successfully"}
