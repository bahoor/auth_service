from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Document):
    email: EmailStr
    hashed_password: str

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def create(cls, email: str, password: str):
        hashed_password = pwd_context.hash(password)
        return cls(email=email, hashed_password=hashed_password)

    class Settings:
        collection = "users"
