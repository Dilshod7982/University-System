from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from auth import hash_password, verify_password
from auth import AuthJWT
from database import get_db

from pydantic import BaseModel

router = APIRouter()

class RegisterModel(BaseModel):
    username: str
    password: str
    role: str  # "student" yoki "teacher"

class LoginModel(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: RegisterModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = Authorize.create_access_token(subject=db_user.id)
    return {"access_token": access_token}

@router.get("/me")
def me(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.id == user_id).first()
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }

@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
