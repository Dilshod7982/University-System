import grpc
from user_pb2_grpc import UserServiceServicer
from user_pb2 import UserResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

class UserService(UserServiceServicer):
    def GetUserById(self, request, context):
        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == request.id).first()
        db.close()

        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return UserResponse()

        return UserResponse(
            id=user.id,
            username=user.username,
            role=user.role
        )
