from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import settings, env_config
from backend.models.roles import ChangeRoleRequestStatus
from backend.schemas.file import File, ImageLink
from backend.helpers.forms import ValidateJsonWithFormBody, form_body
from backend.schemas.links import TelegramUsername, VKUsernameToUrl, YoutubeChannelID, VKUsername, TelegramUsernameToUrl, YoutubeChannelIDToUrl


class UserUsername(BaseModel):
    username: str = Query(
        ...,
        min_length=int(env_config.get('VITE_MIN_LOGIN_LENGTH')),
        max_length=int(env_config.get('VITE_MAX_LOGIN_LENGTH')),
        description='Логин пользователя'
    )


class UserPassword(BaseModel):
    password: str = Query(
        ...,
        min_length=int(env_config.get('VITE_MIN_PASSWORD_LENGTH')),
        max_length=int(env_config.get('VITE_MAX_PASSWORD_LENGTH')),
        description='Пароль пользователя'
    )


class ChangePassword(UserPassword):
    new_password: str = Query(
        ...,
        min_length=int(env_config.get('VITE_MIN_PASSWORD_LENGTH')),
        max_length=int(env_config.get('VITE_MAX_PASSWORD_LENGTH')),
        description='Новый пароль пользователя'
    )


class UserAuth(UserUsername, UserPassword):
    ...


class UserBase(BaseModel):
    first_name: str | None = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_FIRSTNAME_LENGTH')),
        description='Имя пользователя'
    )
    last_name: str | None = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_LASTNAME_LENGTH')),
        description='Фамилия пользователя'
    )


class UserTypes(BaseModel):
    type: settings.USER_ACCOUNT_STATUSES

    class Config:
        use_enum_values = True


class AllUserTypes(BaseModel):
    type: settings.UserTypeEnum

    class Config:
        use_enum_values = True


class UserWithTypeRegister(UserBase, UserAuth, UserTypes):
    ...


class UserRegister(UserBase, UserAuth):
    ...


class UserModifiable(UserBase, ValidateJsonWithFormBody):
    remove_picture: bool = Query(
        ...,
        description='Удалить аватарку пользователя'
    )


class UserInfo(AllUserTypes, UserBase, UserUsername):
    id: int
    picture: ImageLink | None = Query(
        default=None,
        description='Ccылка на аватарку пользователя',
    )

    class Config:
        orm_mode = True


@form_body
class UpdateUserRoleRequest(BaseModel):
    message: str = Query(..., description='Сообщение пользователя')
    requested_account_status: settings.USER_ACCOUNT_STATUSES = Query(
        ..., description='Запрашиваемый статус аккаунта')


class CreateRoleRequestAnswer(BaseModel):
    message: str | None = Query(..., description='Ответное сообщение')
    setted_account_status: settings.USER_ACCOUNT_STATUSES = Query(
        ..., description='Присвоенный статус')

    class Config:
        orm_mode = True


class RoleRequestAnswer(CreateRoleRequestAnswer):
    request_id: int = Query(...,
                            description='ID запроса на изменение типа аккаунта')


class UpdateRoleRequestAnswer(CreateRoleRequestAnswer):
    request_status: ChangeRoleRequestStatus = Query(
        ..., description='Статус запроса')


class TimeCreated(BaseModel):
    time_created: datetime = Query(..., description='Время создания')


class ChangeRoleRequestInfo(TimeCreated):
    files: List[File] = Query(...,
                              description='Файлы, прикрепленные к запросу')
    message: str = Query(..., description='Сообщение пользователя')
    request_status: ChangeRoleRequestStatus = Query(
        ..., description='Статус запроса')
    requested_account_status: settings.USER_ACCOUNT_STATUSES = Query(...,
                                                                     description='Запрашиваемый статус аккаунта')
    answer: RoleRequestAnswer | None = Query(...,
                                             description='Ответ на запрос')

    class Config:
        orm_mode = True


class ChangeRoleRequestFullInfo(ChangeRoleRequestInfo):
    id: int = Query(..., description='ID запроса на изменение типа аккаунта')
    user: UserInfo = Query(..., description='Пользователь, сделавший запрос')

    class Config:
        orm_mode = True


class PublicProfileLinksURLS(BaseModel):

    youtube: YoutubeChannelID = Query(default=None)
    telegram: TelegramUsername = Query(default=None)
    vk: VKUsername = Query(default=None)


class PublicProfileLinks(BaseModel):
    youtube: YoutubeChannelIDToUrl = Query(default=None,
                                           description='Ссылка на канал YouTube')
    telegram: TelegramUsernameToUrl | None = Query(default=None,
                                                   description='Ссылка на канал/аккаунт в Telegram')
    vk: VKUsernameToUrl = Query(
        default=None, description='Ссылка на страницу VK')

    class Config:
        orm_mode = True


class PublicProfileBase(BaseModel):
    name: str = Query(..., description='Оторажаемое имя', max_length=int(
        env_config.get('VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH')
    ), min_length=1)
    description: str | None = Query(default=False, description='Описание профиля', max_length=int(
        env_config.get('VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH')
    ))


class PublicProfile(PublicProfileBase):
    id: int = Query(..., description='ID публичного профиля')
    links: PublicProfileLinks = Query(..., description='Ссылки на соц. сети')
    picture: ImageLink | None

    class Config:
        orm_mode = True


class PublicProfileModifiable(PublicProfileBase, PublicProfileLinksURLS, ValidateJsonWithFormBody):
    remove_picture: bool = Query(
        default=False, description='Удалить аватарку публичного профиля')
