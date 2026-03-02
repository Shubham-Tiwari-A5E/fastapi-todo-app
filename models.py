import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    todos = relationship("Todo", back_populates="user")

class Todo(Base):
    __tablename__ = "todos"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    priority = Column(Integer, nullable=False)
    isCompleted = Column(Boolean, default=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="todos")
