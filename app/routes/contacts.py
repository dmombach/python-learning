from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import Session
from app.db import get_session
from app.schemas import ContactCreate, ContactRead
from app.services import contact_service
from app.auth import get_current_user

router = APIRouter(prefix="/contacts")


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username}


@router.post("/", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    existing = contact_service.get_contact_by_name(session, contact.name)
    if existing:
        raise HTTPException(status_code=400, detail="Contact name already exists.")

    return contact_service.create_contact(session, contact, current_user.id)


@router.get("/", response_model=list[ContactRead])
def list_contacts(
    session: Session = Depends(get_session), current_user=Depends(get_current_user)
):
    return contact_service.get_contacts_by_owner(session, current_user.id)


@router.get("/{name}", response_model=ContactRead)
def get_contact(
    name: str = Path(..., example="Dan M"),
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    contact = contact_service.get_contact_by_name(session, name)
    if not contact or contact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact name not found.")

    return contact


@router.put("/{name}", response_model=ContactRead)
def update_contact(
    contact: ContactCreate,
    name: str = Path(..., example="Dan M"),
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    existing = contact_service.update_contact(session, name, contact)
    if not existing or existing.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found.")

    return existing


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    name: str = Path(..., example="Dan M"),
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    contact = contact_service.get_contact_by_name(session, name)
    if not contact or contact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found.")

    session.delete(contact)
    session.commit()
