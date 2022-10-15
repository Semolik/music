from typing import List
from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from helpers.files import save_file
from helpers.images import set_picture
from schemas.user import UpdateUserRoleRequest, UserInfo, UserModifiableForm, ChangeRoleRequestInfo
from schemas.error import HTTP_401_UNAUTHORIZED
from models.user import File as FileModel
from crud.crud_user import UserCruds
router = APIRouter()
user_cruds = UserCruds()


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(UserData: UserModifiableForm = Depends(UserModifiableForm), userPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    # user_cruds = UserCruds()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_image = save_file(upload_file=userPicture,
                         user_id=db_user.id, force_image=True, resize_image=True)
    db_user_updated = user_cruds.update(
        user=db_user, new_user_data=UserData, userPic=db_image)
    user_data = db_user_updated.as_dict()
    user_data = set_picture(user_data, db_user_updated.picture)
    return user_data


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    user_data = user.as_dict()
    user_data = set_picture(user_data, user.picture)
    return user_data


@router.post('/change-role', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def send_update_role_request(Authorize: AuthJWT = Depends(), formData: UpdateUserRoleRequest = Depends(UpdateUserRoleRequest), files: List[UploadFile] = []):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_files: List[FileModel] = [
        user_cruds.create(
            save_file(
                upload_file=upload_file,
                user_id=current_user_id
            )
        )
        for upload_file in files]
    files_ids = [file.id for file in db_files]
    user_cruds.send_change_role_message(
        user_id=current_user_id, message=formData.message, files_ids=files_ids)
    return {'detail': 'Сообщение отправлено'}


@router.get('/change-role', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=List[ChangeRoleRequestInfo])
def get_change_requests(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    return user_cruds.get_user_change_role_messages(user_id=current_user_id)


@router.get('/has-change-role-requests', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def user_has_change_requests(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    result = user_cruds.is_has_change_role_messages(user_id=current_user_id)
    return result
