from fastapi.testclient import TestClient


def test_post_and_get_student(database_client: TestClient) -> None:

    response = database_client.post(
        "/training_center_api/students/",
        json={
            "full_name": "Brian",
            "email": "brian@mail.com",
            "age": 18,
            "skills": ["python", "rust", "docker", "git", "postgresql"],
            "is_active": True,
        },
    )

    created_student = {
        "id": 1,
        "full_name": "Brian",
        "email": "brian@mail.com",
        "age": 18,
        "skills": ["python", "rust", "docker", "git", "postgresql"],
        "is_active": True,
    }

    assert response.status_code == 201
    assert response.json() == created_student

    student_id = response.json()["id"]

    response = database_client.get(
        f"/training_center_api/students/{student_id}",
    )

    assert response.status_code == 200
    assert response.json() == created_student


def test_clean_database(database_client: TestClient) -> None:

    response = database_client.get(
        "/training_center_api/students",
    )

    assert response.status_code == 200
    assert response.json() == []
