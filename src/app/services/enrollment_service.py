from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.enrollment_repository import (
    insert_enrollment,
    update_enrollment,
)


async def service_make_enrollment(
    session: AsyncSession,
    values: dict[str, object],
):    

    enrollment = await insert_enrollment(
        session=session,
        values=values,
)

    await session.commit()

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

    await session.commit()

    return enrollment


