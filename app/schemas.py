from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    email: str
    phone: str


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
