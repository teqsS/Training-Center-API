from fastapi import APIRouter

from app.dependencies.database import SessionDep
from app.schemas.course import (
    CourseResponseDTO,
)
from app.schemas.student import (
    StudentAddDTO,
    StudentResponseDTO,
    StudentUpdateDTO,
)
from app.services.course_service import (
    service_get_courses_by_student,
)
from app.services.student_service import (
    service_delete_student,
    service_get_student_by_id,
    service_get_students,
    service_insert_student,
    service_update_student,
)

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.get(
    "",
    response_model=list[StudentResponseDTO],
    status_code=200,
    summary="Get all students",
)
async def get_students(
    session: SessionDep,
):

    return await service_get_students(
        session=session,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponseDTO,
    status_code=200,
    summary="Get the student by ID",
)
async def get_student_by_id(
    session: SessionDep,
    student_id: int,
):

    return await service_get_student_by_id(
        session=session,
        student_id=student_id,
    )


@router.get(
    "/{student_id}/courses",
    response_model=list[CourseResponseDTO],
    status_code=200,
    summary="Get the courses the student is enrolled in",
)
async def get_courses_by_student(
    session: SessionDep,
    student_id: int,
):

    return await service_get_courses_by_student(
        session=session,
        student_id=student_id,
    )


@router.post(
    "/",
    status_code=201,
    summary="Add student",
)
async def add_student(
    session: SessionDep,
    student: StudentAddDTO,
):

    return await service_insert_student(
        session=session,
        values=student.model_dump(),
    )


@router.patch(
    "/{student_id}",
    status_code=200,
    summary="Update student details",
)
async def update_student(
    session: SessionDep,
    student_id: int,
    student: StudentUpdateDTO,
):

    values = student.model_dump(exclude_unset=True)

    return await service_update_student(
        session=session,
        student_id=student_id,
        values=values,
    )


@router.delete(
    "/{student_id}",
    status_code=200,
    summary="Delete student",
)
async def delete_student(
    session: SessionDep,
    student_id: int,
):

    return await service_delete_student(
        session=session,
        student_id=student_id,
    )
