from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database import get_db

from schemas.auth import UserRegister
from schemas.auth import UserLogin

from services.auth_service import register_user
from services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
        user: UserRegister,
        db: Session = Depends(get_db)):

    return register_user(user, db)


@router.post("/login")
def login(
        user: UserLogin,
        db: Session = Depends(get_db)):

    return login_user(
        user.username,
        user.password,
        db
    )