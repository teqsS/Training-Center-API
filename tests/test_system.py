from fastapi.testclient import TestClient


def test_get_info(client: TestClient) -> None:

    response = client.get("/training_center_api/")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "name": "training_center_api",
        "version": "0.1.0",
        "status": "is running",
    }
