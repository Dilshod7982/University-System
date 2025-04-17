import grpc
from concurrent import futures
import time

from enrollment_pb2_grpc import add_EnrollmentServiceServicer_to_server
from grpc_server import EnrollmentService

PORT = 50053

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_EnrollmentServiceServicer_to_server(EnrollmentService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"✅ Enrollment gRPC server running on port {PORT}...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
