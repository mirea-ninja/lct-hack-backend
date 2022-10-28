from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr

from app.models.utils import optional


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


@optional
class UserPatch(UserBase):
    pass
