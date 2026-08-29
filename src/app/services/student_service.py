from app.repositories.student_repository import *


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

    return student 

async def service_get_students_by_course(
    session: AsyncSession,
    course_id: int
):

    students = await select_students_by_course(
        session=session,
        course_id=course_id,
    )

    return students

async def service_insert_student(
    session: AsyncSession,
    values: dict[str, object],
):

    result = await insert_student(
        session=session,
        values=values,
    )

    await session.commit()

    return result

async def service_update_student(
    session: AsyncSession,
    student_id: int,
    values: dict[str, object],
):

    result = await update_student(
        session=session,
        student_id=student_id,
        values=values,
    )

    await session.commit()

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

    await session.commit()

    return result



