from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from schemas.auth import UserRegister
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token


def register_user(user: UserRegister, db: Session):

    existing = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(username: str, password: str, db: Session):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }