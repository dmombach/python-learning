from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.contacts import add_contact, list_contacts, search_contact
from app.db import get_db
from app.services.contact_service import add_contact, find_contact, list_contacts

router = APIRouter()


class Contact(BaseModel):
    name: str
    phone: str


@router.post("/contacts", status_code=status.HTTP_201_CREATED)
def create_contact(contact: Contact, db=Depends(get_db)):
    if any(c["name"] == contact.name for c in db["contacts"]):
        raise HTTPException(status_code=400, detail="Contact already exists.")

    db["contacts"].append(contact.model_dump())
    return {"message": "Contact added."}


@router.get("/contacts")
def get_contacts(db=Depends(get_db)):
    return db["contacts"]


@router.get("/contacts/{name}")
def get_contact(name: str, db=Depends(get_db)):
    for c in db["contacts"]:
        if c["name"] == name:
            return c
    raise HTTPException(status_code=404, detail="Contact not found.")
