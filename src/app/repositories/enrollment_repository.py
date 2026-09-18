from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    EnrollmentsOrm,
)
from app.models.enrollment import Status


async def select_quantity_enrollments(
    session: AsyncSession,
    course_id: int,
):

    query = select(func.count(EnrollmentsOrm.id)).where(
        EnrollmentsOrm.status == Status.active,
        EnrollmentsOrm.course_id == course_id,
    )

    result = await session.execute(query)

    return result.scalar_one()


async def select_and_block_enrollment(
    session: AsyncSession,
    enrollment_id: int,
):

    query = (
        select(EnrollmentsOrm)
        .where(EnrollmentsOrm.id == enrollment_id)
        .with_for_update()
    )

    result = await session.execute(query)

    return result.scalar()


async def insert_enrollment(
    session: AsyncSession,
    values: dict[str, int],
):

    enrollment = EnrollmentsOrm(**values)

    session.add(enrollment)
    await session.flush()

    return enrollment


async def update_enrollment(
    session: AsyncSession,
    enrollment_id: int,
    values: dict[str, object],
):

    stmt = (
        update(EnrollmentsOrm)
        .filter(EnrollmentsOrm.id == enrollment_id)
        .values(**values)
        .returning(EnrollmentsOrm)
    )

    result = await session.execute(stmt)

    return result.scalar_one_or_none()
