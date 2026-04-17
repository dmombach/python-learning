from sqlmodel import select
from app.models import Contact


def create_contact(session, contact_data):
    contact = Contact(**contact_data.model_dump())
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


def get_all_contacts(session):
    return session.exec(select(Contact)).all()


def get_contact_by_name(session, name: str):
    statement = select(Contact).where(Contact.name == name)
    return session.exec(statement).first()


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
