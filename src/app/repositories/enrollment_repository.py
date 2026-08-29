from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    EnrollmentsOrm,
)


async def insert_enrollment(
    session: AsyncSession,
    values: dict[str, object],
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

