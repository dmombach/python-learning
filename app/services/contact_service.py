from sqlmodel import select
from app.models import Contact
from app.schemas import ContactCreate


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
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact
