from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.course import CoursesOrm
    from app.models.student import StudentsOrm

from app.models.base import Base, created_at, intpk, updated_at


class Status(enum.Enum):

    active = "active"
    cancelled = "cancelled"
    completed = "completed"


class EnrollmentsOrm(Base):
    __tablename__ = "enrollments"

    id: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    status: Mapped[Status]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    student: Mapped[StudentsOrm] = relationship(back_populates="enrollments")
    course: Mapped[CoursesOrm] = relationship(back_populates="enrollments")

    __table_args__ = (
        Index(
            "uq_enrollments_active_student_course",
            "student_id",
            "course_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )