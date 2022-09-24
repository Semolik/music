from fastapi import Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from schemas.user import UserInfo
from models.error import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm.session import Session
from db.db import get_db
from crud.crud_user import get_user_by_username
router = APIRouter()


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def protected(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = get_user_by_username(db, current_user)
    return user.as_dict()
