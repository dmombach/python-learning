from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.db import get_session
from app.services import user_service
from app.auth import create_access_token, get_current_user
from app.security import verify_password
from app.schemas import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = user_service.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    user = user_service.create_user(session, user_data)
    if not user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    return user
