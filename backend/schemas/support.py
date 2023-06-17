from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import Query
import uuid
from backend.core.config import env_config
from backend.schemas.user import UserInfo
from backend.models.support import SupportMessageStatus, SupportMessageType


class SupportMessageBase(BaseModel):
    email: str = Query(..., description="Email пользователя",
                       max_length=int(env_config.get('MAX_EMAIL_LENGTH')))
    message: str = Query(..., description="Сообщение", max_length=int(
        env_config.get('MAX_SUPPORT_MESSAGE_LENGTH')))
    type: SupportMessageType = Query(
        default=SupportMessageType.SUPPORT,
        description="Тип сообщения"
    )


class CreateSupportMessage(SupportMessageBase):

    login: str = Query(..., description="Логин пользователя")


class SupportMessage(SupportMessageBase):
    id: uuid.UUID = Query(..., description="ID сообщения")
    status: SupportMessageStatus = Query(
        ...,
        description="Статус сообщения"
    )

    created_at: datetime = Query(...,
                                 description="Дата создания сообщения")

    class Config:
        orm_mode = True


class SupportMessageLogin(SupportMessage):
    login: str = Query(..., description="Логин пользователя")

    class Config:
        orm_mode = True


class SupportMessageFull(SupportMessage):
    user: UserInfo

    class Config:
        orm_mode = True
