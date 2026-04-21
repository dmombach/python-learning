from sqlmodel import Session, select
from app.models import User
from app.security import hash_password
from app.schemas import UserCreate
from app.models import User


def create_user(session: Session, data: UserCreate):
    # Check if username already exists
    existing = get_user_by_username(session, data.username)
    if existing:
        return None

    user = User(username=data.username, hashed_password=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()
