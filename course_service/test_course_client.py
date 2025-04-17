import grpc
from course_pb2 import CreateCourseRequest, CourseIdRequest
from course_pb2_grpc import CourseServiceStub


def create_course(stub):
    request = CreateCourseRequest(
        name="Advanced Python",
        description="Deep dive into Python programming",
        teacher_id=1  # bu user_service da ro'yxatdan o'tgan teacher bo'lishi kerak
    )
    try:
        response = stub.CreateCourse(request)
        print("✅ Course created:")
        print(response)
        return response.id
    except grpc.RpcError as e:
        print(f"❌ CreateCourse error: {e.code()} - {e.details()}")


def get_course(stub, course_id):
    request = CourseIdRequest(id=course_id)
    try:
        response = stub.GetCourse(request)
        print("📘 Course details:")
        print(response)
    except grpc.RpcError as e:
        print(f"❌ GetCourse error: {e.code()} - {e.details()}")


def delete_course(stub, course_id):
    request = CourseIdRequest(id=course_id)
    try:
        stub.DeleteCourse(request)
        print(f"🗑 Course with id {course_id} deleted successfully.")
    except grpc.RpcError as e:
        print(f"❌ DeleteCourse error: {e.code()} - {e.details()}")


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = CourseServiceStub(channel)

        # 1. Create course
        course_id = create_course(stub)
        if not course_id:
            return

        # 2. Get course
        get_course(stub, course_id)

        # 3. Delete course
        delete_course(stub, course_id)


if __name__ == "__main__":
    run()
