from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CoursesOrm,
    EnrollmentsOrm,
    StudentsOrm,
)


async def select_students(
    session: AsyncSession,
):
    query = (
        select(StudentsOrm)
        .where(StudentsOrm.is_active.is_(True))
    )

    result = await session.execute(query)

    return result.scalars().all()

async def select_student_by_id(
    session: AsyncSession,
    student_id: int,
):
    
    query = (
        select(StudentsOrm)
        .where(
            StudentsOrm.id == student_id,
            StudentsOrm.is_active.is_(True),
        )
    )
    result = await session.execute(query)

    return result.scalar()

async def select_students_by_course(
    session: AsyncSession,
    course_id: int,
):

    query = (
        select(StudentsOrm)
        .where(
            CoursesOrm.is_active.is_(True),
            StudentsOrm.is_active.is_(True),
            StudentsOrm.enrollments.any(
                and_(
                    EnrollmentsOrm.course_id == course_id,
                    EnrollmentsOrm.status == "active",
                )
            )
        )
    )

    result = await session.execute(query)

    return result.scalars().all()

async def insert_student(
    session: AsyncSession,
    values: dict[str, object],
):
    
    student = StudentsOrm(**values)

    session.add(student)
    await session.flush()

    return student

async def update_student(
    session: AsyncSession,
    student_id: int,
    values: dict[str, object],      
):
    
    stmt = (
        update(StudentsOrm)
        .filter(StudentsOrm.id == student_id)
        .values(**values)
        .returning(StudentsOrm)
    )

    result = await session.execute(stmt)

    return result.scalar_one_or_none()

