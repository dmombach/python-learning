from pydantic import BaseModel
from datetime import datetime


class ContactBase(BaseModel):
    name: str
    email: str
    phone: str


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str


class ContactListResponse(BaseModel):
    total: int
    items: list[ContactRead]
