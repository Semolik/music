from uuid import UUID
from backend.helpers.auth_helper import Authenticate
from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from backend.core.config import settings
from backend.schemas.support import CreateSupportMessage, SupportMessageLogin, SupportMessageFull
from backend.crud.crud_support import SupportCrud
from backend.crud.crud_user import UserCruds
from backend.models.support import SupportMessageType, SupportMessageStatus
router = APIRouter(tags=['Поддержка'], prefix='/support')


@router.post('/messages', status_code=status.HTTP_201_CREATED, response_model=SupportMessageLogin)
def create_support_message(
    support_message: CreateSupportMessage,
    auth: Authenticate = Depends(Authenticate(required=False))
):
    db_user = UserCruds(auth.db).get_user_by_username(
        username=support_message.login)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    if auth.current_user and auth.current_user.id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя создавать сообщения от чужого имени"
        )
    return SupportCrud(auth.db).create_support_message(
        user_id=db_user.id,
        email=support_message.email,
        message=support_message.message,
        type=support_message.type
    )


@router.get('/messages/{message_id}', response_model=SupportMessageLogin)
def get_support_message(
    message_id: UUID = Path(..., description="ID сообщения"),
    auth: Authenticate = Depends(Authenticate(required=False))
):
    db_support_message = SupportCrud(auth.db).get_message_by_id(message_id)
    if not db_support_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено"
        )
    if auth.current_user and auth.current_user_id != db_support_message.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя получать сообщения от чужого имени"
        )
    return db_support_message


@router.get('/messages', response_model=list[SupportMessageLogin])
def get_support_messages(
    type: SupportMessageType = None,
    page: int = Query(1, description="Номер страницы", gt=0),
    auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    return SupportCrud(auth.db).get_messages(type=type, page=page)


@router.put('/messages/{message_id}', response_model=SupportMessageLogin)
def update_support_message(
    message_id: UUID = Path(..., description="ID сообщения"),
    message_status: SupportMessageStatus = Query(
        ..., description="Статус сообщения"),
    auth: Authenticate = Depends(Authenticate(is_admin=True))
):
    db_support_message = SupportCrud(auth.db).get_message_by_id(message_id)
    if not db_support_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено"
        )
    return SupportCrud(auth.db).update_support_message(
        db_message=db_support_message,
        status=message_status
    )
