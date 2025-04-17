from sqlalchemy.orm import Session
import grpc
from enrollment_pb2_grpc import EnrollmentServiceServicer
from enrollment_pb2 import EnrollResponse, StudentListResponse, Student
import models
import database


class EnrollmentService(EnrollmentServiceServicer):
    def __init__(self):
        models.Base.metadata.create_all(bind=database.engine)

    def EnrollStudent(self, request, context):
        db: Session = database.SessionLocal()

        # Student allaqachon shu kursga yozilganmi? Tekshiramiz
        existing = db.query(models.Enrollment).filter_by(
            student_id=request.student_id,
            course_id=request.course_id
        ).first()

        if existing:
            db.close()
            return EnrollResponse(
                enrollment_id=existing.id,
                message="Student is already enrolled in this course"
            )

        enrollment = models.Enrollment(
            student_id=request.student_id,
            course_id=request.course_id
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        db.close()

        return EnrollResponse(
            enrollment_id=enrollment.id,
            message="Student enrolled successfully"
        )

    def GetEnrolledStudents(self, request, context):
        db: Session = database.SessionLocal()
        enrollments = db.query(models.Enrollment).filter_by(
            course_id=request.course_id
        ).all()
        db.close()

        return StudentListResponse(
            students=[
                Student(
                    id=e.id,
                    student_id=e.student_id,
                    course_id=e.course_id
                ) for e in enrollments
            ]
        )
