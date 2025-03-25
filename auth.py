from fastapi import APIRouter, HTTPException, Depends
from models import User
from database import get_db
from jwt_utils import create_access_token
from pydantic import BaseModel, EmailStr
from datetime import timedelta

auth_router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str

@auth_router.post("/register")
async def register(user: UserRegister, db=Depends(get_db)):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User.create(email=user.email, password=user.password)
    await new_user.insert()
    return {"message": "User created successfully"}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@auth_router.post("/login")
async def login(user: UserLogin):
    db_user = await User.find_one(User.email == user.email)
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(db_user.id)}, timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}
