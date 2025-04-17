import grpc
from sqlalchemy.orm import Session
from course_pb2_grpc import CourseServiceServicer
from course_pb2 import CourseResponse, CourseIdRequest, CreateCourseRequest, Empty
from models import Course
import database
from user_client import get_user_by_id


class CourseService(CourseServiceServicer):
    def __init__(self):
        # Baza jadvalini yaratish (agar hali bo'lmasa)
        Course.metadata.create_all(bind=database.engine)

    def CreateCourse(self, request: CreateCourseRequest, context):
        user = get_user_by_id(request.teacher_id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Teacher not found")
            return CourseResponse()

        if user["role"] != "teacher":
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Only teachers can create courses")
            return CourseResponse()

        db: Session = database.SessionLocal()
        new_course = Course(
            name=request.name,
            description=request.description,
            teacher_id=request.teacher_id
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        db.close()

        return CourseResponse(
            id=new_course.id,
            name=new_course.name,
            description=new_course.description,
            teacher_id=new_course.teacher_id
        )

    def GetCourse(self, request: CourseIdRequest, context):
        db: Session = database.SessionLocal()
        course = db.query(Course).filter(Course.id == request.id).first()
        db.close()

        if not course:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Course not found")
            return CourseResponse()

        return CourseResponse(
            id=course.id,
            name=course.name,
            description=course.description,
            teacher_id=course.teacher_id
        )

    def DeleteCourse(self, request: CourseIdRequest, context):
        db: Session = database.SessionLocal()
        course = db.query(Course).filter(Course.id == request.id).first()

        if not course:
            db.close()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Course not found")
            return Empty()

        db.delete(course)
        db.commit()
        db.close()
        return Empty()
