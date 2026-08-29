from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.student import StudentSkill


class StudentAddDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    age: int = Field(ge=16, le=100)
    skills: list[StudentSkill] = Field(default_factory=list)
    is_active: bool = Field(default=True)


class StudentResponseDTO(StudentAddDTO):
    model_config = ConfigDict(extra="forbid")

    id: int


class StudentUpdateDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, min_length=3, max_length=120)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=16, le=100)
    skills: list[StudentSkill] | None = None
    is_active: bool | None = None
