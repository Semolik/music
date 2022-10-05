from fastapi import Depends, APIRouter, status, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from helpers.images import save_image
from schemas.user import UserInfo, UserModifiableForm
from schemas.error import HTTP_401_UNAUTHORIZED
from crud.crud_user import UserCruds
router = APIRouter()


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(UserData: UserModifiableForm = Depends(UserModifiableForm), userPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_cruds = UserCruds()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    db_image = save_image(upload_file=userPicture, user=db_user)
    db_user_updated = user_cruds.update(
        user=db_user, new_user_data=UserData, userPic=db_image)
    return db_user_updated.as_dict()


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user = UserCruds().get_user_by_id(current_user_id)
    return user.as_dict()
