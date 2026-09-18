from fastapi import APIRouter

from app.dependencies.database import SessionDep
from app.schemas.enrollment import (
    EnrollmentAddDTO,
    EnrollmentResponseDTO,
)
from app.schemas.error import ErrorResponseDTO
from app.services.enrollment_service import (
    service_cancel_enrollment,
    service_complete_enrollment,
    service_make_enrollment,
)

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)


@router.post(
    "/",
    response_model=EnrollmentResponseDTO,
    responses={
        409: {"model": ErrorResponseDTO},
        404: {"model": ErrorResponseDTO},
    },
    status_code=201,
    summary="Make enrollment",
)
async def make_enrollment(session: SessionDep, enrollment: EnrollmentAddDTO):

    return await service_make_enrollment(
        session=session,
        values=enrollment.model_dump(),
    )


@router.patch(
    "/{enrollment_id}/complete",
    response_model=EnrollmentResponseDTO,
    responses={
        404: {"model": ErrorResponseDTO},
        409: {"model": ErrorResponseDTO},
    },
    status_code=200,
    summary="Complete the course",
)
async def complete_enrollement(
    session: SessionDep,
    enrollment_id: int,
):

    return await service_complete_enrollment(
        session=session,
        enrollment_id=enrollment_id,
    )


@router.delete(
    "/{enrollment_id}",
    response_model=EnrollmentResponseDTO,
    responses={
        404: {"model": ErrorResponseDTO},
        409: {"model": ErrorResponseDTO},
    },
    status_code=200,
    summary="Cancel the course",
)
async def cancel_enrollment(
    session: SessionDep,
    enrollment_id: int,
):

    return await service_cancel_enrollment(
        session=session,
        enrollment_id=enrollment_id,
    )
