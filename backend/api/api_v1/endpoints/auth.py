from typing import Any
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from models.error import HTTP_401_UNAUTHORIZED
from core.security import authenticate
from sqlalchemy.orm.session import Session
from db.db import get_db
from schemas.user import UserAuth
from crud.crud_user import create_user
from sqlalchemy.orm import Session
from schemas.user import UserRegister
from models.user import Users as users_model
router = APIRouter()

@router.post('/login', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def login(user: UserAuth, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = authenticate(username=user.username, password=user.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return user.as_dict()


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


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
            detail="Такой пользователь уже существует",
        )
    user = create_user(db=db, user=user_in)
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return user.as_dict()
