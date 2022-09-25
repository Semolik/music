from fastapi import Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from schemas.user import UserInfo, UserModifiable
from models.error import HTTP_401_UNAUTHORIZED
from sqlalchemy.orm.session import Session
from db.db import get_db
from crud.crud_user import get_user_by_username, update_user
router = APIRouter()


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(UserData: UserModifiable, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = get_user_by_username(db=db, username=current_user)
    user = update_user(db=db,  user=user, new_user_data=UserData)
    return user.as_dict()


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = get_user_by_username(db, current_user)
    return user.as_dict()
