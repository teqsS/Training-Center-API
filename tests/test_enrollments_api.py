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


def test_post_rejects_system_fields(database_client: TestClient) -> None:

    enrollment = {
        "course_id": 1,
        "student_id": 1,
        "status": "active",
    }

    response = database_client.post(
        "/training_center_api/enrollments/",
        json=enrollment,
    )

    assert response.status_code == 422
