from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class APICallBase(BaseModel):
    ip_address: str
    country: str
    weather_state: str
    temperature: float

class APICallCreate(APICallBase):
    pass

class APICall(APICallBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    task_name: str
    description: str
    status: Optional[str] = "pendiente"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    task_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TaskDelete(BaseModel):
    message: str