from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enrollment import Status


class EnrollmentAddDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    student_id: int
    course_id: int


class EnrollmentResponseDTO(EnrollmentAddDTO):
    model_config = ConfigDict(extra="forbid")

    id: int
    status: Status
    created_at: datetime
    updated_at: datetime
