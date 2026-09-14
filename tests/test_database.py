from fastapi.testclient import TestClient


def test_clean_database(database_client: TestClient) -> None:

    response = database_client.get(
        "/training_center_api/students",
    )

    assert response.status_code == 200
    assert response.json() == []
