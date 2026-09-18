from fastapi.testclient import TestClient


def create_test_course(
    database_client: TestClient,
    **overrides: object,
) -> dict[str, object]:

    course = {
        "name": "Go Backend",
        "teacher": "Jaire Alexander",
        "description": "Go lang backend development",
        "price": 20000,
        "capacity": 30,
        "level": "intermediate",
    }

    course.update(overrides)

    response = database_client.post(
        "/training_center_api/courses/",
        json=course,
    )

    assert response.status_code == 201

    return response.json()


def create_test_student(
    database_client: TestClient,
    **overrides: object,
) -> dict[str, object]:

    student = {
        "full_name": "Brian",
        "email": "brian@mail.com",
        "age": 18,
        "skills": ["python", "rust", "docker", "git", "postgresql"],
    }

    student.update(overrides)

    response = database_client.post(
        "/training_center_api/students/",
        json=student,
    )

    assert response.status_code == 201

    return response.json()


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


def test_create_enrollment(database_client: TestClient) -> None:

    course = create_test_course(database_client)
    student = create_test_student(database_client)

    json_enrollment = {
        "course_id": course["id"],
        "student_id": student["id"],
    }

    response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["status"] == "active"
    assert response.json()["student_id"] == json_enrollment["student_id"]
    assert response.json()["course_id"] == json_enrollment["course_id"]
    assert "created_at" in response.json()
    assert "updated_at" in response.json()


def test_create_enrollment_with_missing_student(database_client: TestClient) -> None:

    course = create_test_course(database_client)

    json_enrollment = {
        "course_id": course["id"],
        "student_id": 999999,
    }

    response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == f"Student with id {json_enrollment['student_id']} not found"
    )


def test_create_enrollment_with_missing_course(database_client: TestClient) -> None:

    student = create_test_student(database_client)

    json_enrollment = {
        "course_id": 999999,
        "student_id": student["id"],
    }

    response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == f"Course with id {json_enrollment['course_id']} not found"
    )


def test_create_existing_enrollment(database_client: TestClient) -> None:

    course = create_test_course(database_client)
    student = create_test_student(database_client)

    json_enrollment = {
        "course_id": course["id"],
        "student_id": student["id"],
    }

    response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response.status_code == 201

    existing_enrollment_response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert existing_enrollment_response.status_code == 409
    assert (
        existing_enrollment_response.json()["detail"]
        == f"Active enrollment with course id {course['id']} and student id {student['id']} already exists"
    )


def test_enroll_deactivated_student(database_client: TestClient) -> None:

    student = create_test_student(database_client)
    course = create_test_course(database_client)

    deactivate_student_response = database_client.delete(
        f"/training_center_api/students/{student['id']}",
    )

    assert deactivate_student_response.status_code == 200

    json_enrollment = {
        "student_id": student["id"],
        "course_id": course["id"],
    }

    enrollment_response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert enrollment_response.status_code == 404
    assert (
        enrollment_response.json()["detail"]
        == f"Student with id {student['id']} not found"
    )


def test_enroll_deactivated_course(database_client: TestClient) -> None:

    student = create_test_student(database_client)
    course = create_test_course(database_client)

    deactivate_course_response = database_client.delete(
        f"/training_center_api/courses/{course['id']}",
    )

    assert deactivate_course_response.status_code == 200

    json_enrollment = {
        "student_id": student["id"],
        "course_id": course["id"],
    }

    enrollment_response = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert enrollment_response.status_code == 404
    assert (
        enrollment_response.json()["detail"]
        == f"Course with id {course['id']} not found"
    )


def test_enroll_max_capacity_course(database_client: TestClient) -> None:

    course = create_test_course(database_client, capacity=1)

    student_1 = create_test_student(database_client, email="Brian@gmail.com")
    student_2 = create_test_student(database_client, email="Jared@gmail.com")

    enrollment = {
        "student_id": student_1["id"],
        "course_id": course["id"],
    }

    enroll_student1_response = database_client.post(
        "/training_center_api/enrollments/",
        json=enrollment,
    )

    assert enroll_student1_response.status_code == 201

    enrollment = {
        "student_id": student_2["id"],
        "course_id": course["id"],
    }

    enroll_student2_response = database_client.post(
        "/training_center_api/enrollments/",
        json=enrollment,
    )

    assert enroll_student2_response.status_code == 409
    assert (
        enroll_student2_response.json()["detail"]
        == f"Course with id {course['id']} has reached its capacity"
    )


def test_complete_enrollment_and_reenroll(database_client: TestClient) -> None:

    course = create_test_course(database_client)
    student = create_test_student(database_client)

    json_enrollment = {
        "student_id": student["id"],
        "course_id": course["id"],
    }

    response_post = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response_post.status_code == 201
    assert response_post.json()["id"] == 1
    assert response_post.json()["status"] == "active"

    response_patch = database_client.patch(
        f"/training_center_api/enrollments/{response_post.json()['id']}/complete",
    )

    assert response_patch.status_code == 200
    assert response_patch.json()["status"] == "completed"

    response_post = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response_post.status_code == 201
    assert response_post.json()["id"] == 2
    assert response_post.json()["status"] == "active"


def test_cancel_enrollment_and_reenroll(database_client: TestClient) -> None:

    course = create_test_course(database_client)
    student = create_test_student(database_client)

    json_enrollment = {
        "student_id": student["id"],
        "course_id": course["id"],
    }

    response_post = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response_post.status_code == 201
    assert response_post.json()["id"] == 1
    assert response_post.json()["status"] == "active"

    response_delete = database_client.delete(
        f"/training_center_api/enrollments/{response_post.json()['id']}",
    )

    assert response_delete.status_code == 200
    assert response_delete.json()["status"] == "cancelled"

    response_post = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response_post.status_code == 201
    assert response_post.json()["id"] == 2
    assert response_post.json()["status"] == "active"


def test_cancel_completed_enrollment(database_client: TestClient) -> None:

    course = create_test_course(database_client)
    student = create_test_student(database_client)

    json_enrollment = {
        "student_id": student["id"],
        "course_id": course["id"],
    }

    response_post = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response_post.status_code == 201
    assert response_post.json()["id"] == 1
    assert response_post.json()["status"] == "active"

    response_patch = database_client.patch(
        f"/training_center_api/enrollments/{response_post.json()['id']}/complete",
    )

    assert response_patch.status_code == 200
    assert response_patch.json()["status"] == "completed"

    response_delete = database_client.delete(
        f"/training_center_api/enrollments/{response_post.json()['id']}",
    )

    assert response_delete.status_code == 409
    assert response_delete.json()["detail"] == (
        f"Enrollment with id {response_post.json()['id']} cannot transition from completed to cancelled"
    )


def test_complete_cancelled_enrollment(database_client: TestClient) -> None:

    course = create_test_course(database_client)
    student = create_test_student(database_client)

    json_enrollment = {
        "student_id": student["id"],
        "course_id": course["id"],
    }

    response_post = database_client.post(
        "/training_center_api/enrollments/",
        json=json_enrollment,
    )

    assert response_post.status_code == 201
    assert response_post.json()["id"] == 1
    assert response_post.json()["status"] == "active"

    response_delete = database_client.delete(
        f"/training_center_api/enrollments/{response_post.json()['id']}",
    )

    assert response_delete.status_code == 200
    assert response_delete.json()["status"] == "cancelled"

    response_patch = database_client.patch(
        f"/training_center_api/enrollments/{response_post.json()['id']}/complete",
    )

    assert response_patch.status_code == 409
    assert response_patch.json()["detail"] == (
        f"Enrollment with id {response_post.json()['id']} cannot transition from cancelled to completed"
    )
