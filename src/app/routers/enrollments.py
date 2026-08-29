from fastapi import APIRouter

from app.dependencies.database import SessionDep
from app.schemas.enrollment import *
from app.services.enrollment_service import *

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)

@router.post(
    "/",
    status_code=200,
    summary="Make enrollment",
)
async def make_enrollment(
    session: SessionDep,
    enrollment: EnrollmentAddDTO
):

    return (
        await service_make_enrollment(
            session=session,
            values=enrollment.model_dump(),
        )
    )

@router.patch(
    "/{enrollment_id}/complete",
    status_code=200,
    summary="Complete the course",
)
async def complete_enrollement(
    session: SessionDep,
    enrollment_id: int,
):

    return (
        await service_complete_enrollment(
            session=session,
            enrollment_id=enrollment_id,
        )
    )

@router.delete(
    "/{enrollment_id}",
    status_code=200,
    summary="Cancel the course",
)
async def cancel_enrollment(
    session: SessionDep,
    enrollment_id: int,
):

    return (
        await service_cancel_enrollment(
            session=session,
            enrollment_id=enrollment_id,
        )
    )
