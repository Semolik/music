from fastapi import Depends, APIRouter, status
from fastapi_jwt_auth import AuthJWT
from schemas.user import UserInfo, UserModifiable
from models.error import HTTP_401_UNAUTHORIZED
from crud.crud_user import user_cruds
router = APIRouter()


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(UserData: UserModifiable, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_username(username=current_user)
    db_user_updated = user_cruds.update(user=db_user, new_user_data=UserData)
    return db_user_updated.as_dict()


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = user_cruds.get_user_by_username(current_user)
    return user.as_dict()
