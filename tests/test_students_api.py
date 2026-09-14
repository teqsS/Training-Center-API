from fastapi.testclient import TestClient


def test_get_missing_student(database_client: TestClient) -> None:

    student_id = 999999

    response = database_client.get(
        f"/training_center_api/students/{student_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Student with id {student_id} not found"


def test_post_repeated_email(database_client: TestClient) -> None:

    json_1 = {
        "full_name": "Brian",
        "email": "brian@mail.com",
        "age": 18,
        "skills": ["python", "rust", "docker", "git", "postgresql"],
        "is_active": True,
    }

    response_1 = database_client.post(
        "/training_center_api/students/",
        json=json_1,
    )

    assert response_1.status_code == 201

    json_2 = {
        "full_name": "Jahmyr",
        "email": "brian@mail.com",
        "age": 20,
        "skills": ["go", "redis", "docker", "git", "postgresql", "kubernetes"],
        "is_active": True,
    }

    response_2 = database_client.post(
        "/training_center_api/students/",
        json=json_2,
    )

    assert response_2.status_code == 409
    assert (
        response_2.json()["detail"]
        == f"Student with email {json_2['email']} already exists"
    )


def test_post_and_get_student(database_client: TestClient) -> None:

    response_post = database_client.post(
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

    assert response_post.status_code == 201
    assert response_post.json() == created_student

    response_get = database_client.get(
        f"/training_center_api/students/{response_post.json()['id']}",
    )

    assert response_get.status_code == 200
    assert response_get.json() == created_student


def test_patch_missing_student(database_client: TestClient) -> None:

    student_id = 999999
    json = {
        "full_name": "Jameson",
        "email": "Jamo@mail.com",
        "age": 21,
        "skills": ["c", "rust", "git"],
        "is_active": True,
    }

    response = database_client.patch(
        f"/training_center_api/students/{student_id}",
        json=json,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Student with id {student_id} not found"


def test_deactivate_missing_student(database_client: TestClient) -> None:

    student_id = 999999

    response = database_client.delete(
        f"/training_center_api/students/{student_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Student with id {student_id} not found"


def test_patch_repeated_student_email(database_client: TestClient) -> None:

    json_1 = {
        "full_name": "Brian",
        "email": "brian@mail.com",
        "age": 18,
        "skills": ["python", "rust", "docker", "git", "postgresql"],
        "is_active": True,
    }

    response_post_1 = database_client.post(
        "/training_center_api/students/",
        json=json_1,
    )

    json_1 = {
        "id": response_post_1.json()["id"],
        **json_1,
    }

    assert response_post_1.status_code == 201
    assert response_post_1.json() == json_1

    json_2 = {
        "full_name": "Jahmyr",
        "email": "Jahmyr@mail.com",
        "age": 20,
        "skills": ["go", "redis", "docker", "git", "postgresql", "kubernetes"],
        "is_active": True,
    }

    response_post_2 = database_client.post(
        "/training_center_api/students/",
        json=json_2,
    )

    json_2 = {
        "id": response_post_2.json()["id"],
        **json_2,
    }

    assert response_post_2.status_code == 201
    assert response_post_2.json() == json_2

    json_3 = {
        "email": "Jahmyr@mail.com",
    }

    response_patch = database_client.patch(
        f"/training_center_api/students/{json_1['id']}",
        json=json_3,
    )

    assert response_patch.status_code == 409
    assert (
        response_patch.json()["detail"]
        == f"Student with email {json_3['email']} already exists"
    )
