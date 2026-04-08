from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from app.db import get_session
from app.schemas import ContactCreate, ContactRead
from app.services import contact_service

router = APIRouter(prefix="/contacts")


@router.post("/", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, session: Session = Depends(get_session)):
    existing = contact_service.get_contact_by_name(session, contact.name)
    if existing:
        raise HTTPException(status_code=400, detail="Contact name already exists.")
    return contact_service.create_contact(session, contact)


@router.get("/", response_model=list[ContactRead])
def list_contacts(session: Session = Depends(get_session)):
    return contact_service.get_all_contacts(session)


@router.get("/{name}", response_model=ContactRead)
def get_contact(name: str, session: Session = Depends(get_session)):
    contact = contact_service.get_contact_by_name(session, name)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact name not found.")
    return contact
