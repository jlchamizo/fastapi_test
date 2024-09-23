from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class APICall(Base):
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String)
    country = Column(String)
    weather_state = Column(String)
    temperature = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pendiente")
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())