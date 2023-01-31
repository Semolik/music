from typing import List
from fastapi import Depends, APIRouter, status, UploadFile, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from backend.helpers.files import save_file
from backend.helpers.validate_role import validate_admin
from backend.schemas.user import TimeCreated, UpdateRoleRequestAnswer, UpdateUserRoleRequest, ChangeRoleRequestFullInfo, ChangeRoleRequestInfo
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.models.files import File
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_change_roles import ChangeRolesCruds
from backend.crud.crud_user import UserCruds
router = APIRouter(tags=['Роли'])


@router.post('/change-role', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, status_code=status.HTTP_201_CREATED)
def send_update_role_request(
    formData: UpdateUserRoleRequest = Depends(),
    Authorize: AuthJWT = Depends(),
    files: List[UploadFile] = [],
    db: Session = Depends(get_db)
):
    '''Отправка запроса на смену типа аккаунта'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if UserCruds(db).is_admin(user_id=current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Ошибка. Администратор не может отправить запрос на смену типа аккаунта"
        )
    if ChangeRolesCruds(db).is_user_have_active_change_role_messages(user_id=current_user_id, count=settings.ACTIVE_CHANGE_ROLE_REQUESTS_COUNT):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Ошибка. Одновременно возможно иметь только {settings.ACTIVE_CHANGE_ROLE_REQUESTS_COUNT} активных запроса на смену типа аккаунта"
        )
    if UserCruds(db).get_user_by_id(user_id=current_user_id).type == formData.account_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"При отправке запроса небходимо выбрать статус, отличный от текущего")
    db_files: List[File] = [
        save_file(
            db=db,
            upload_file=upload_file,
            user_id=current_user_id
        )
        for upload_file in files]
    return ChangeRolesCruds(db).send_change_role_message(
        user_id=current_user_id, message=formData.message, files=db_files, account_status=formData.account_status)


@router.get('/change-role', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=List[ChangeRoleRequestInfo])
def get_change_requests(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Получение списка запросов на смену типа аккаунта'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    return ChangeRolesCruds(db).get_user_change_role_messages(user_id=current_user_id)


@router.get('/change-role/has', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=bool)
def user_has_change_requests(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Проверка наличия запросов на смену типа аккаунта'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    return ChangeRolesCruds(db).is_has_change_role_messages(user_id=current_user_id)


@router.get('/change-role/all', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=List[ChangeRoleRequestFullInfo])
def get_all_change_role_requests(
    page: int = Query(1, description='Номер страницы'),
    filter: settings.ALLOWED_STATUSES_FILTER = Query(
        settings.ALLOWED_STATUSES_LIST[-1],
        description='Фильтр по статусу'
    ),
        Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Получение списка запросов на смену типа аккаунта от всех пользователей'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not UserCruds(db).is_admin(user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    return ChangeRolesCruds(db).get_all_change_role_messages(page=page, filter=filter)


@router.post('/change-role/{request_id}/answer', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=TimeCreated)
def send_update_role_request_answer(request_id: int, data: UpdateRoleRequestAnswer, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Ответ на запрос на смену типа аккаунта'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(db=db, user_id=current_user_id)
    db_request = ChangeRolesCruds(db).get_change_role_message(
        request_id=request_id)
    if not db_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Запрос на смену типа аккаута по данному id не найден")
    answer_obj = ChangeRolesCruds(db).send_change_role_message_answer(
        request=db_request, message=data.message, request_status=data.request_status, account_status=data.status)
    return answer_obj
