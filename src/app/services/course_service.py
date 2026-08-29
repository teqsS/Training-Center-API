from app.repositories.course_repository import *


async def service_get_courses(
    session: AsyncSession,
):

    courses = await select_courses(
        session=session,
    )

    return courses

async def service_get_course_by_id(
    session: AsyncSession,
    course_id: int,
):

    course = await select_course_by_id(
        session=session,
        course_id=course_id,
    )

    return course

async def service_get_courses_by_student(
    session: AsyncSession,
    student_id: int,
):

    courses = await select_courses_by_student(
        session=session,
        student_id=student_id,
    )

    return courses

async def service_insert_course(
    session: AsyncSession,
    values: dict[str, object],
):

    course = await insert_course(
        session=session,
        values=values,
    )

    await session.commit()

    return course

async def service_update_course(
    session: AsyncSession,
    course_id: int,
    values: dict[str, object],
):

    course = await update_course(
        session=session,
        course_id=course_id,
        values=values,
    )

    await session.commit()

    return course

async def service_cancel_course(
    session: AsyncSession,
    course_id: int,
):

    result = await update_course(
        session=session,
        course_id=course_id,
        values={"is_active": False}
    )

    await session.commit()
        
    return result



