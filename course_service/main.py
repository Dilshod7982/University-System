import grpc
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from concurrent import futures
from course_pb2_grpc import add_CourseServiceServicer_to_server
from grpc_server import CourseService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CourseServiceServicer_to_server(CourseService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ Course gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()