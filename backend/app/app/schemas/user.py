from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_superuser: bool = False
    full_name: str
    phone_number: Optional[int] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    uuid: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
