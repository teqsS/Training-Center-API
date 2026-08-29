from fastapi import APIRouter

from app.dependencies.database import SessionDep
from app.schemas.course import (
    CourseAddDTO,
    CourseChangeDTO,
    CourseResponseDTO,
)
from app.schemas.student import (
    StudentResponseDTO,
)
from app.services.course_service import (
    service_cancel_course,
    service_get_course_by_id,
    service_get_courses,
    service_insert_course,
    service_update_course,
)
from app.services.student_service import service_get_students_by_course

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.get(
    "",
    response_model=list[CourseResponseDTO],
    status_code=200,
    summary="Get all courses",
)
async def get_courses(
    session: SessionDep,
):

    return await service_get_courses(
        session=session,
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponseDTO,
    status_code=200,
    summary="Get the course by ID",
)
async def get_course_by_id(
    session: SessionDep,
    course_id: int,
):

    return await service_get_course_by_id(
        session=session,
        course_id=course_id,
    )


@router.get(
    "/{course_id}/students",
    response_model=list[StudentResponseDTO],
    status_code=200,
    summary="Get all students enrolled in the course",
)
async def get_students_by_course(
    session: SessionDep,
    course_id: int,
):

    return await service_get_students_by_course(
        session=session,
        course_id=course_id,
    )


@router.post(
    "/",
    response_model=CourseResponseDTO,
    status_code=201,
    summary="Add course",
)
async def add_course(
    session: SessionDep,
    course: CourseAddDTO,
):

    return await service_insert_course(
        session=session,
        values=course.model_dump(),
    )


@router.patch(
    "/{course_id}",
    status_code=200,
    summary="Update course details",
)
async def update_course(
    session: SessionDep,
    course_id: int,
    course: CourseChangeDTO,
):

    values = course.model_dump(exclude_unset=True)

    return await service_update_course(
        session=session,
        course_id=course_id,
        values=values,
    )


@router.delete(
    "/{course_id}",
    status_code=200,
    summary="Delete course",
)
async def cancel_course(
    session: SessionDep,
    course_id: int,
):

    return await service_cancel_course(
        session=session,
        course_id=course_id,
    )
