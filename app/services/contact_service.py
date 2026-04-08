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
