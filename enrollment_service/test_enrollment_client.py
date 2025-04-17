import grpc
from enrollment_pb2 import EnrollRequest, CourseIdRequest
from enrollment_pb2_grpc import EnrollmentServiceStub


def enroll_student(stub):
    request = EnrollRequest(student_id=2, course_id=4)  # mavjud student va kurs ID lar
    response = stub.EnrollStudent(request)
    print(f"✅ EnrollStudent: {response.message} (ID: {response.enrollment_id})")
    return request.course_id


def get_enrolled_students(stub, course_id):
    request = CourseIdRequest(course_id=course_id)
    response = stub.GetEnrolledStudents(request)
    print(f"\n📘 Enrolled students in course {course_id}:")
    for student in response.students:
        print(f" - EnrollmentID: {student.id}, StudentID: {student.student_id}")


def run():
    with grpc.insecure_channel("localhost:50053") as channel:
        stub = EnrollmentServiceStub(channel)

        course_id = enroll_student(stub)
        get_enrolled_students(stub, course_id)


if __name__ == "__main__":
    run()
