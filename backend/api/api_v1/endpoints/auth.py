from typing import Any
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import validate_authorized_user
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.user import ChangePassword, UserAuth, UserInfo, UserPassword
from backend.crud.crud_user import UserCruds
from backend.schemas.user import UserRegister
router = APIRouter(tags=['Авторизация'], prefix='/auth')


@router.post('/login', response_model=UserInfo, responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def login(user_in: UserAuth, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Авторизация пользователя'''
    db_user = UserCruds(db).login(user_in)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    access_token = Authorize.create_access_token(subject=db_user.id)
    refresh_token = Authorize.create_refresh_token(subject=db_user.id)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return db_user


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    '''Выход из системы'''
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    '''Обновление токена'''
    Authorize.jwt_refresh_token_required()
    current_user_id = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user_id)
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@router.post("/signup", response_model=UserInfo, status_code=201)
def create_user_signup(user_in: UserRegister, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> Any:
    """
    Создание пользователя без необходимости последующей авторизации
    """
    user_exists = UserCruds(db).get_user_by_username(user_in.username)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="Такой пользователь уже существует",
        )
    db_user = UserCruds(db).create_user(user_in)
    access_token = Authorize.create_access_token(subject=db_user.id)
    refresh_token = Authorize.create_refresh_token(subject=db_user.id)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return db_user


@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(passwords: ChangePassword, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    Изменение пароля пользователя
    """
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db)
    user_cruds = UserCruds(db)
    if not user_cruds.check_password(db_user, passwords.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль",
        )
    if user_cruds.get_password_hash(passwords.new_password) == db_user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Новый пароль совпадает со старым",
        )
    user_cruds.change_password(user=db_user,
                               new_password=passwords.new_password)
