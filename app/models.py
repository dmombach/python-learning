from sqlmodel import SQLModel, Field
from typing import Optional


class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
