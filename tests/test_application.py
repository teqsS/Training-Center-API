from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application import create_app
from app.config import Settings


def test_create_app_returns_independent_instances(settings: Settings) -> None:

    app_1 = create_app(settings)
    app_2 = create_app(settings)

    assert app_1 is not app_2


def test_applications_have_isolated_database_resources(settings: Settings) -> None:

    app_1 = create_app(settings)
    app_2 = create_app(settings)

    with TestClient(app_1), TestClient(app_2):
        assert app_1.state.engine is not app_2.state.engine
        assert app_1.state.session_factory is not app_2.state.session_factory


def test_openapi_includes_expected_paths(app: FastAPI) -> None:

    schema = app.openapi()

    actual_paths = set(schema["paths"])
    expected_paths = {
        "/training_center_api/",
        "/training_center_api/courses",
        "/training_center_api/courses/",
        "/training_center_api/courses/{course_id}",
        "/training_center_api/courses/{course_id}/students",
        "/training_center_api/students",
        "/training_center_api/students/",
        "/training_center_api/students/{student_id}",
        "/training_center_api/students/{student_id}/courses",
        "/training_center_api/enrollments/",
        "/training_center_api/enrollments/{enrollment_id}",
        "/training_center_api/enrollments/{enrollment_id}/complete",
    }

    assert expected_paths.issubset(actual_paths)
    assert (
        "201"
        in schema["paths"]["/training_center_api/enrollments/"]["post"]["responses"]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/courses/{course_id}"]["get"][
            "responses"
        ]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/courses/{course_id}"]["patch"][
            "responses"
        ]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/courses/{course_id}"]["delete"][
            "responses"
        ]
    )
    assert (
        "409" in schema["paths"]["/training_center_api/students/"]["post"]["responses"]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/students/{student_id}"]["get"][
            "responses"
        ]
    )
    assert {"404", "409"}.issubset(
        schema["paths"]["/training_center_api/students/{student_id}"]["patch"][
            "responses"
        ]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/students/{student_id}"]["delete"][
            "responses"
        ]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/enrollments/{enrollment_id}"][
            "delete"
        ]["responses"]
    )
    assert (
        "404"
        in schema["paths"]["/training_center_api/enrollments/{enrollment_id}/complete"][
            "patch"
        ]["responses"]
    )

    assert (
        "#/components/schemas/ErrorResponseDTO"
        == schema["paths"]["/training_center_api/courses/{course_id}"]["get"][
            "responses"
        ]["404"]["content"]["application/json"]["schema"]["$ref"]
    )
