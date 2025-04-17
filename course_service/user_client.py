import grpc
from user_pb2_grpc import UserServiceStub
from user_pb2 import UserIdRequest

def get_user_by_id(user_id: int):
    try:
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = UserServiceStub(channel)
            response = stub.GetUserById(UserIdRequest(id=user_id))
            return {
                "id": response.id,
                "username": response.username,
                "role": response.role
            }
    except grpc.RpcError as e:
        print(f"❌ gRPC error: {e.code()} - {e.details()}")
        return None
