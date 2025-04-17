import grpc
import uvicorn
import multiprocessing

from fastapi import FastAPI
from routes import router
from database import Base, engine
from auth import auth_exception_handler
from user_pb2_grpc import add_UserServiceServicer_to_server
from grpc_server import UserService
from concurrent import futures
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.exception_handler(AuthJWTException)
def jwt_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("✅ gRPC user_service running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    grpc_process = multiprocessing.Process(target=serve_grpc)
    grpc_process.start()
    print("🚀 FastAPI user_service running on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
