from typing import List
from fastapi import Depends, APIRouter, status, UploadFile, HTTPException, Query
from backend.core.config import settings
from backend.helpers.files import save_file, valid_content_length
from backend.models.roles import ChangeRoleRequestStatus
from backend.schemas.user import RoleRequestAnswer, UpdateRoleRequestAnswer, UpdateUserRoleRequest, ChangeRoleRequestFullInfo
from backend.models.files import File
from backend.crud.crud_change_roles import ChangeRolesCruds
from backend.helpers.auth_helper import Authenticate
router = APIRouter(tags=['Роли'], prefix='/roles/change')


@router.post('', status_code=status.HTTP_201_CREATED, dependencies=[Depends(valid_content_length(settings.MAX_CHANGE_ROLE_FILES_SIZE_MB))], response_model=ChangeRoleRequestFullInfo)
def send_update_role_request(
    formData: UpdateUserRoleRequest = Depends(),
    Auth: Authenticate = Depends(Authenticate()),
    files: List[UploadFile] = [],

):
    '''Отправка запроса на смену типа аккаунта'''

    if Auth.current_user.type == settings.UserTypeEnum.superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Ошибка. Администратор не может отправить запрос на смену типа аккаунта"
        )
    change_role_cruds = ChangeRolesCruds(db=Auth.db)
    if change_role_cruds.user_have_active_change_role_request(user_id=Auth.current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Ошибка. Одновременно возможно иметь только один активный запрос на смену типа аккаунта"
        )
    if Auth.current_user.type == settings.UserTypeEnum.musician:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Вы уже имеете статус музыканта"
        )
    db_files: List[File] = [
        save_file(
            db=Auth.db,
            upload_file=upload_file,
            user_id=Auth.current_user_id
        )
        for upload_file in files]
    return change_role_cruds.send_change_role_message(
        user_id=Auth.current_user_id,
        message=formData.message,
        files=db_files
    )


@router.get('', response_model=List[ChangeRoleRequestFullInfo])
def get_change_requests(
    page: int = Query(1, description='Номер страницы', ge=1),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение списка запросов на смену типа аккаунта'''
    return ChangeRolesCruds(Auth.db).get_user_change_role_messages(user_id=Auth.current_user_id, page=page)


@router.get('/has', response_model=bool)
def has_change_requests(
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Имеется ли запросы на смену типа аккаунта'''

    return ChangeRolesCruds(Auth.db).user_have_change_role_request(user_id=Auth.current_user_id)


@router.get('/current', response_model=ChangeRoleRequestFullInfo | None)
def get_current_change_request(
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение текущего запроса на смену типа аккаунта'''
    message = ChangeRolesCruds(Auth.db).get_current_user_change_role_message(
        user_id=Auth.current_user_id)
    if not message:
        return
    return message


@router.get('/all', response_model=List[ChangeRoleRequestFullInfo])
def get_all_change_role_requests(
    page: int = Query(1, description='Номер страницы', ge=1),
    filter: ChangeRoleRequestStatus = Query(default=None,
                                            description='Фильтр по статусу'),
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Получение списка запросов на смену типа аккаунта от всех пользователей'''
    messages = ChangeRolesCruds(Auth.db).get_all_change_role_messages(
        page=page, filter=filter)

    return messages


@router.get('/{request_id}', response_model=ChangeRoleRequestFullInfo)
def get_change_role_request(request_id: int, Auth: Authenticate = Depends(Authenticate(is_admin=True))):
    '''Получение запроса на смену типа аккаунта'''
    message = ChangeRolesCruds(Auth.db).get_change_role_message(
        request_id=request_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Запрос на смену типа аккаута по данному id не найден")
    return message


@router.delete('/{request_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_change_role_request(request_id: int, Auth: Authenticate = Depends(Authenticate())):
    '''Удаление запроса на смену типа аккаунта'''
    message = ChangeRolesCruds(Auth.db).get_change_role_message(
        request_id=request_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Запрос на смену типа аккаута по данному id не найден")
    if message.user_id != Auth.current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете удалить запрос на смену типа аккаунта другого пользователя")
    if message.request_status != ChangeRoleRequestStatus.in_progress:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Нельзя удалить запрос на смену типа аккаунта, который уже был обработан")

    ChangeRolesCruds(Auth.db).delete(message)
    return


@router.post('/{request_id}/answer', response_model=RoleRequestAnswer)
def send_update_role_request_answer(request_id: int, data: UpdateRoleRequestAnswer,  Auth: Authenticate = Depends(Authenticate(is_admin=True))):
    '''Ответ на запрос на смену типа аккаунта'''
    db_request = ChangeRolesCruds(Auth.db).get_change_role_message(
        request_id=request_id)
    if not db_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Запрос на смену типа аккаута по данному id не найден")
    answer = ChangeRolesCruds(Auth.db).send_change_role_message_answer(
        request=db_request,
        message=data.message,
        request_status=data.request_status
    )
    return answer
