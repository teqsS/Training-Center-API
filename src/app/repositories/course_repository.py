from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import *


async def select_courses(
    session: AsyncSession,
):
    
    query = (
        select(CoursesOrm)
        .where(CoursesOrm.is_active.is_(True))
    )

    result = await session.execute(query)

    return result.scalars().all()

async def select_course_by_id(
    session: AsyncSession,
    course_id: int,
):
    
    query = (
        select(CoursesOrm)
        .where(
            CoursesOrm.id == course_id,
            CoursesOrm.is_active.is_(True),
        )
    )

    result = await session.execute(query)

    return result.scalar()

async def select_courses_by_student(
    session: AsyncSession,
    student_id: int,
):
    
    query = (
    select(CoursesOrm)
    .where(
        CoursesOrm.is_active.is_(True),
        StudentsOrm.is_active.is_(True),
        CoursesOrm.enrollments.any(
            and_(
                EnrollmentsOrm.student_id == student_id,
                EnrollmentsOrm.status == Status.active,
            )
        )
    )
)

    result = await session.execute(query)

    return result.scalars().all()

async def insert_course(
    session: AsyncSession,
    values: dict[str, object],
):
    
    course = CoursesOrm(**values)

    session.add(course)
    await session.flush()

    return course

async def update_course(
    session: AsyncSession,
    course_id: int,
    values: dict[str, object],
):
    
    stmt = (
        update(CoursesOrm)
        .where(CoursesOrm.id == course_id)
        .values(**values)
        .returning(CoursesOrm)
    )

    result = await session.execute(stmt)

    return result.scalar_one_or_none()

