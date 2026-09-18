from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    ActiveEnrollmentAlreadyExistsError,
    CourseCapacityReachedError,
    CourseNotFoundError,
    EnrollmentNotFoundError,
    StudentNotFoundError,
)
from app.repositories.course_repository import (
    select_and_block_active_course,
)
from app.repositories.enrollment_repository import (
    insert_enrollment,
    select_quantity_enrollments,
    update_enrollment,
)
from app.repositories.student_repository import select_student_by_id


async def service_make_enrollment(
    session: AsyncSession,
    values: dict[str, int],
):

    check_existence_student_result = await select_student_by_id(
        session=session,
        student_id=values["student_id"],
    )
    if check_existence_student_result is None:
        raise StudentNotFoundError(values["student_id"])

    course = await select_and_block_active_course(
        session=session,
        course_id=values["course_id"],
    )
    if course is None:
        raise CourseNotFoundError(values["course_id"])

    course_enrollments_quantity = await select_quantity_enrollments(
        session=session,
        course_id=values["course_id"],
    )
    if course_enrollments_quantity >= course.capacity:
        raise CourseCapacityReachedError(values["course_id"])

    try:
        enrollment = await insert_enrollment(
            session=session,
            values=values,
        )

        await session.commit()

    except IntegrityError as error:
        sqlstate = getattr(error.orig, "sqlstate", None)

        driver_error = getattr(error.orig, "__cause__", None)
        constraint_name = getattr(driver_error, "constraint_name", None)

        if (
            sqlstate == "23505"
            and constraint_name == "uq_enrollments_active_student_course"
        ):
            raise ActiveEnrollmentAlreadyExistsError(
                student_id=values["student_id"],
                course_id=values["course_id"],
            ) from error

        raise

    return enrollment


async def service_complete_enrollment(
    session: AsyncSession,
    enrollment_id: int,
):

    enrollment = await update_enrollment(
        session=session,
        enrollment_id=enrollment_id,
        values={"status": "completed"},
    )

    if enrollment is None:
        raise EnrollmentNotFoundError(enrollment_id)

    await session.commit()

    return enrollment


async def service_cancel_enrollment(
    session: AsyncSession,
    enrollment_id: int,
):

    enrollment = await update_enrollment(
        session=session,
        enrollment_id=enrollment_id,
        values={"status": "cancelled"},
    )

    if enrollment is None:
        raise EnrollmentNotFoundError(enrollment_id)

    await session.commit()

    return enrollment
