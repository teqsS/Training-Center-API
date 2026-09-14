from typing import cast

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    StudentEmailAlreadyExistsError,
    StudentNotFoundError,
)
from app.repositories.student_repository import (
    insert_student,
    select_student_by_id,
    select_students,
    select_students_by_course,
    update_student,
)


async def service_get_students(
    session: AsyncSession,
):

    students = await select_students(
        session=session,
    )

    return students


async def service_get_student_by_id(
    session: AsyncSession,
    student_id: int,
):

    student = await select_student_by_id(
        session=session,
        student_id=student_id,
    )

    if student is None:
        raise StudentNotFoundError(student_id)

    return student


async def service_get_students_by_course(session: AsyncSession, course_id: int):

    students = await select_students_by_course(
        session=session,
        course_id=course_id,
    )

    return students


async def service_insert_student(
    session: AsyncSession,
    values: dict[str, object],
):

    try:
        result = await insert_student(
            session=session,
            values=values,
        )

        await session.commit()

    except IntegrityError as error:
        sqlstate = getattr(error.orig, "sqlstate", None)

        driver_error = getattr(error.orig, "__cause__", None)
        constraint_name = getattr(driver_error, "constraint_name", None)

        if sqlstate == "23505" and constraint_name == "uq_check_email":
            raise StudentEmailAlreadyExistsError(cast(str, values["email"])) from error

        raise

    return result


async def service_update_student(
    session: AsyncSession,
    student_id: int,
    values: dict[str, object],
):

    try:
        result = await update_student(
            session=session,
            student_id=student_id,
            values=values,
        )

        if result is None:
            raise StudentNotFoundError(student_id)

        await session.commit()

    except IntegrityError as error:
        sqlstate = getattr(error.orig, "sqlstate", None)

        driver_error = getattr(error.orig, "__cause__", None)
        constraint_name = getattr(driver_error, "constraint_name", None)

        if sqlstate == "23505" and constraint_name == "uq_check_email":
            raise StudentEmailAlreadyExistsError(cast(str, values["email"])) from error

        raise

    return result


async def service_delete_student(
    session: AsyncSession,
    student_id: int,
):

    result = await update_student(
        session=session,
        student_id=student_id,
        values={"is_active": False},
    )

    if result is None:
        raise StudentNotFoundError(student_id)

    await session.commit()

    return result
