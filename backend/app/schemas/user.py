from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Shared Properties
class UserBase(BaseModel):
    email: EmailStr
    username: str


# Properties to recieve via API on creation
class UserCreate(UserBase):
    password: str


# Properties to recieve via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Allows reading form ORM models


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties stored in DB (includes hashed_password)
class UserInDB(UserInDBBase):
    hashed_password: str
