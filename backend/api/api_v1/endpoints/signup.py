from fastapi import Depends, APIRouter, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from db.db import get_db
from schemas.user import UserRegister
from models.user import Users as users_model
from crud.crud_user import create_user
from typing import Any
router = APIRouter()


@router.post("/signup", status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(get_db),
    user_in: UserRegister,
    Authorize: AuthJWT = Depends()
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = db.query(users_model).filter(
        users_model.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = create_user(db=db, user=user_in)
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return user.as_dict()
