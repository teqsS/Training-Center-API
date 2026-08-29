from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Enum,
    String,
    UniqueConstraint,
    text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.course import CoursesOrm
    from app.models.enrollment import EnrollmentsOrm

from app.models.base import Base, intpk


class StudentSkill(str, enum.Enum):
    python = "python"
    rust = "rust"
    c = "c"
    go = "go"
    java = "java"
    fastapi = "fastapi"
    postgresql = "postgresql"
    docker = "docker"
    git = "git"
    sqlalchemy = "sqlalchemy"
    redis = "redis"
    kubernetes = "kubernetes"


student_skill_enum = Enum(
    StudentSkill,
    name="student_skill",
)


class StudentsOrm(Base):
    __tablename__ = "students"

    id: Mapped[intpk]
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str]
    age: Mapped[int]
    skills: Mapped[list[StudentSkill]] = mapped_column(
        ARRAY(student_skill_enum),
        nullable=False,
        default=list,
        server_default=text("'{}'::student_skill[]"),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
        nullable=False,
    )

    enrollments: Mapped[list[EnrollmentsOrm]] = relationship(back_populates="student")
    courses: Mapped[list[CoursesOrm]] = relationship(
        secondary="enrollments",
        back_populates="students",
        viewonly=True,
    )

    __table_args__ = (
        CheckConstraint(
            "char_length(full_name) >= 3",
            name="check_name_length",
        ),
        CheckConstraint(
            "age >= 16 AND age <= 100",
            name="check_age",
        ),
        UniqueConstraint(
            "email",
            name="uq_check_email",
        ),
    )
