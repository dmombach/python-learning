from sqlmodel import select
from app.models import Contact, ContactUpdate
from app.schemas import ContactCreate
from sqlalchemy import or_, asc, desc, func
from fastapi import HTTPException, status
from datetime import datetime, timezone


def create_contact(session, contact_data: ContactCreate, owner_id: int):
    contact = Contact(**contact_data.model_dump(), owner_id=owner_id)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def get_all_contacts(session):
    return session.exec(select(Contact)).all()


def get_contact_by_name(session, name: str):
    statement = select(Contact).where(Contact.name == name)
    return session.exec(statement).first()


def get_contacts_by_owner(session, owner_id: int):
    return session.query(Contact).filter(Contact.owner_id == owner_id).all()


def update_contact(session, name, data):
    contact = get_contact_by_name(session, name)
    if not contact:
        return None

    for key, value in data.model_dump().items():
        setattr(contact, key, value)
    contact.updated_at = datetime.now(timezone.utc)

    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def update_contact(
    session, owner_id: int, contact_id: int, contact_update: ContactUpdate
):
    contact = session.get(Contact, contact_id)
    if not contact or contact.owner_id != contact_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found."
        )

    update_data = contact_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(contact, field, value)
    contact.updated_at = datetime.utcnow()

    session.add(contact)
    session.commit()
    session.refresh(contact)

    return contact


def search_contacts(
    session,
    owner_id: int,
    name=None,
    email=None,
    phone=None,
    sort_by=None,
    sort_order="asc",
    limit=None,
    offset=None,
):
    base = select(Contact).where(Contact.owner_id == owner_id)

    conditions = []

    if name:
        conditions.append(Contact.name.contains(name))
    if email:
        conditions.append(Contact.email.contains(email))
    if phone:
        conditions.append(Contact.phone.contains(phone))

    if conditions:
        query = base.where(or_(*conditions))
    else:
        query = base

    total = session.exec(select(func.count()).select_from(query.subquery())).one()

    if sort_by in {"name", "email", "phone"}:
        column = getattr(Contact, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    items = session.exec(query).all()

    return {"total": total, "items": items}
