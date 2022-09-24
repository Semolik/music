from fastapi import HTTPException, Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from models.error import HTTP_401_UNAUTHORIZED
from core.security import authenticate
from sqlalchemy.orm.session import Session
from db.db import get_db
from schemas.user import UserAuth
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
    return {"msg": "Successfully login"}
