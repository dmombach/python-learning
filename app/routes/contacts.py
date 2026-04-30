from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import Session
from app.db import get_session
from app.schemas import ContactCreate, ContactRead, ContactListResponse
from app.services import contact_service
from app.auth import get_current_user
from app.models import ContactUpdate

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


@router.get("/", response_model=ContactListResponse)
def list_contacts(
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
    limit: int | None = None,
    offset: int | None = None,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return contact_service.search_contacts(
        session=session,
        owner_id=current_user.id,
        name=name,
        email=email,
        phone=phone,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


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


@router.patch("/{contact_id}", response_model=ContactRead)
def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return contact_service.update_contact(
        session=session,
        owner_id=current_user.id,
        contact_id=contact_id,
        contact_update=contact_update,
    )
