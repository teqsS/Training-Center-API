from pydantic import BaseModel, ConfigDict, Field

from app.models.course import CourseLevel


class CourseAddDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=100)
    teacher: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=1000)
    price: int = Field(ge=0)
    capacity: int = Field(default=100, ge=1, le=500)
    level: CourseLevel = CourseLevel.beginner


class CourseResponseDTO(CourseAddDTO):
    model_config = ConfigDict(extra="forbid")

    id: int
    is_active: bool


class CourseChangeDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=3, max_length=100)
    teacher: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=1000)
    price: int | None = Field(default=None, ge=0)
    capacity: int | None = Field(default=None, ge=1, le=500)
    level: CourseLevel | None = None
