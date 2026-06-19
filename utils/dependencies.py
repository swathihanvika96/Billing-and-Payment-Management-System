from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database import get_db

from models.user import User

from utils.jwt import verify_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    payload = verify_token(token)

    if payload is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid Token"

        )

    username = payload.get("sub")

    user = db.query(User).filter(

        User.username == username

    ).first()

    if user is None:

        raise HTTPException(

            status_code=401,

            detail="User not found"

        )

    return user


def get_current_admin(

    current_user: User = Depends(get_current_user)

):

    if current_user.role.lower() != "admin":

        raise HTTPException(

            status_code=403,

            detail="Admin access required"

        )

    return current_user


def get_current_customer(

    current_user: User = Depends(get_current_user)

):

    if current_user.role.lower() != "customer":

        raise HTTPException(

            status_code=403,

            detail="Customer access required"

        )

    return current_user