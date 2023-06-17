from uuid import UUID
from backend.helpers.auth_helper import Authenticate
from fastapi import Depends, APIRouter, HTTPException, Path, status
from backend.core.config import settings
from backend.schemas.support import SupportMessage, CreateSupportMessage, SupportMessageLogin
from backend.crud.crud_support import SupportCrud
from backend.crud.crud_user import UserCruds
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
        message=support_message.message
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
