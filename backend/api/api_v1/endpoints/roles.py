from typing import List
from fastapi import Depends, APIRouter, status, UploadFile, HTTPException
from fastapi_jwt_auth import AuthJWT
from helpers.files import save_file

from schemas.user import UpdateUserRoleRequest, ChangeRoleRequestFullInfo, ChangeRoleRequestInfo
from schemas.error import HTTP_401_UNAUTHORIZED
from models.user import File as FileModel
from crud.crud_user import UserCruds
router = APIRouter()
user_cruds = UserCruds()


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
    return user_cruds.is_has_change_role_messages(user_id=current_user_id)


@router.get('/change-role-requests', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=List[ChangeRoleRequestFullInfo])
def get_all_change_role_requests(page: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not user_cruds.is_admin(user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    return user_cruds.get_all_change_role_messages(page=page)


@router.post('/change-role-answer', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def send_update_role_request(Authorize: AuthJWT = Depends(), formData: UpdateUserRoleRequest = Depends(UpdateUserRoleRequest), files: List[UploadFile] = []):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not user_cruds.is_admin(user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    # АБОБИЧ ДОПИШИ ЗДЕСЬ
