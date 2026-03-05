from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone_number: Optional[str] = None  # WhatsApp number with country code (e.g., +919876543210)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone_number: Optional[str] = None

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
    task_time: Optional[datetime] = None  # When the task should be done
    notification_enabled: bool = True  # Enable 10-minute reminder

class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str] = None
    priority: int
    isCompleted: bool
    task_time: Optional[datetime] = None
    notification_enabled: bool  # Required field, no default in response
    notification_sent: bool  # Whether reminder notification was sent
    completed_at: Optional[datetime] = None
