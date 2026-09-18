from app.models.enrollment import Status


class TrainingCenterError(Exception):
    pass


class NotFoundError(TrainingCenterError):
    pass


class ConflictError(TrainingCenterError):
    pass


class StudentNotFoundError(NotFoundError):
    def __init__(self, student_id: int) -> None:
        self.student_id = student_id
        super().__init__(f"Student with id {student_id} not found")


class CourseNotFoundError(NotFoundError):
    def __init__(self, course_id: int) -> None:
        self.course_id = course_id
        super().__init__(f"Course with id {course_id} not found")


class EnrollmentNotFoundError(NotFoundError):
    def __init__(self, enrollment_id: int) -> None:
        self.enrollment_id = enrollment_id
        super().__init__(f"Enrollment with id {enrollment_id} not found")


class StudentEmailAlreadyExistsError(ConflictError):
    def __init__(self, student_email: str) -> None:
        self.email = student_email
        super().__init__(f"Student with email {student_email} already exists")


class ActiveEnrollmentAlreadyExistsError(ConflictError):
    def __init__(self, student_id: int, course_id: int) -> None:
        self.student_id = student_id
        self.course_id = course_id
        super().__init__(
            f"Active enrollment with course id {course_id} and student id {student_id} already exists"
        )


class CourseCapacityReachedError(ConflictError):
    def __init__(self, course_id: int) -> None:
        self.course_id = course_id
        super().__init__(f"Course with id {course_id} has reached its capacity")


class InvalidEnrollmentStatusTransitionError(ConflictError):
    def __init__(
        self, enrollment_id: int, existed_status: Status, status: Status
    ) -> None:
        self.enrollment_id = enrollment_id
        self.existed_status = existed_status
        self.status = status
        super().__init__(
            f"Enrollment with id {enrollment_id} cannot transition from {existed_status.value} to {status.value}"
        )
