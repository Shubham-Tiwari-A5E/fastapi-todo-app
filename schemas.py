from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int
    isCompleted: bool = False

class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str] = None
    priority: int
    isCompleted: bool
    completed_at: Optional[datetime] = None
