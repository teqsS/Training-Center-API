from fastapi.testclient import TestClient


def test_get_missing_course(database_client: TestClient) -> None:

    course_id = 999999

    response = database_client.get(f"/training_center_api/courses/{course_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Course with id {course_id} not found"


def test_post_and_get_course(database_client: TestClient) -> None:

    response_post = database_client.post(
        "/training_center_api/courses/",
        json={
            "name": "Go Backend",
            "teacher": "Jaire Alexander",
            "description": "Go lang backend development",
            "price": 20000,
            "capacity": 30,
            "level": "intermediate",
            "is_active": True,
        },
    )

    created_course = {
        "id": 1,
        "name": "Go Backend",
        "teacher": "Jaire Alexander",
        "description": "Go lang backend development",
        "price": 20000,
        "capacity": 30,
        "level": "intermediate",
        "is_active": True,
    }

    assert response_post.status_code == 201
    assert response_post.json() == created_course

    response_get = database_client.get(
        f"/training_center_api/courses/{created_course['id']}"
    )

    assert response_get.status_code == 200
    assert response_get.json() == created_course


def test_patch_missing_course(database_client: TestClient) -> None:

    course_id = 999999
    json = {
        "name": "Go Backend",
        "teacher": "Jaire Alexander",
        "description": "Go lang backend development",
        "price": 20000,
        "capacity": 30,
        "level": "intermediate",
        "is_active": True,
    }

    response = database_client.patch(
        f"/training_center_api/courses/{course_id}",
        json=json,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Course with id {course_id} not found"


def test_deactivate_missing_course(database_client: TestClient) -> None:

    course_id = 999999

    response = database_client.delete(f"/training_center_api/courses/{course_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Course with id {course_id} not found"
