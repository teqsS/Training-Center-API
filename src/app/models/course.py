from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.enrollment import EnrollmentsOrm
    from app.models.student import StudentsOrm

from app.models.base import Base, intpk


class CourseLevel(enum.Enum):

    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class CoursesOrm(Base):
    __tablename__ = "courses"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))
    teacher: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000)) 
    price: Mapped[int]
    capacity: Mapped[int]
    level: Mapped[CourseLevel]
    is_active: Mapped[bool]

    enrollments: Mapped[list[EnrollmentsOrm]] = relationship(
        back_populates="course",
    )
    students: Mapped[list[StudentsOrm]] = relationship(
        secondary="enrollments",
        back_populates="courses",
        viewonly=True,
    )

    __table_args__ = (
        CheckConstraint(
            "char_length(name) >= 3",
            name="check_name_length",
        ),
        CheckConstraint(
            "char_length(teacher) >= 3",
            name="check_teacher_length",
        ),
        CheckConstraint(
            "char_length(description) >= 10",
            name="check_description_length",
        ),
        CheckConstraint(
            "price >= 0",
            name="check_price",
        ),
        CheckConstraint(
            "capacity >= 1 and capacity <= 500",
            name="check_capacity",
        )
    )
