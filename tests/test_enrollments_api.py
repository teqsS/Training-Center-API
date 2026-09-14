from fastapi.testclient import TestClient


def test_complete_missing_enrollment(database_client: TestClient) -> None:

    enrollment_id = 999999

    response = database_client.patch(
        f"/training_center_api/enrollments/{enrollment_id}/complete",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Enrollment with id {enrollment_id} not found"


def test_cancel_missing_enrollment(database_client: TestClient) -> None:

    enrollment_id = 999999

    response = database_client.delete(
        f"/training_center_api/enrollments/{enrollment_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Enrollment with id {enrollment_id} not found"
