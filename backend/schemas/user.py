from typing import List, Tuple, Optional, Union
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import settings, env_config
from backend.schemas.file import File
from backend.helpers.forms import ValidateJsonWithFormBody, form_body
from backend.schemas.links import TelegramUsername, YoutubeChannelID, VKUsername


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
    type: settings.ALL_USER_ACCOUNT_STATUSES


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
    picture: str | None = Query(
        default=None,
        description='Ccылка на аватарку пользователя',
    )


@form_body
class UpdateUserRoleRequest(BaseModel):
    message: str = Query(..., description='Сообщение пользователя')
    account_status: settings.USER_ACCOUNT_STATUSES = Query(
        ..., description='Запрашиваемый статус аккаунта')


class CreateRoleRequestAnswer(BaseModel):
    message: str | None = Query(..., description='Ответное сообщение')
    status: str | None = Query(..., description='Присвоенный статус')


class RoleRequestAnswer(CreateRoleRequestAnswer):
    request_id: int = Query(...,
                            description='ID запроса на изменение типа аккаунта')


class UpdateRoleRequestAnswer(CreateRoleRequestAnswer):
    request_status: settings.ALLOWED_STATUSES = Query(
        ..., description='Статус запроса')


class TimeCreated(BaseModel):
    time_created: str = Query(..., description='Время создания')


class ChangeRoleRequestInfo(TimeCreated):
    files: List[File] = Query(...,
                              description='Файлы, прикрепленные к запросу')
    message: str = Query(..., description='Сообщение пользователя')
    status: settings.ALLOWED_STATUSES = Query(...,
                                              description='Статус запроса')
    account_status: str = Query(...,
                                description='Запрашиваемый статус аккаунта')
    answer: RoleRequestAnswer | None = Query(...,
                                             description='Ответ на запрос')


class ChangeRoleRequestFullInfo(ChangeRoleRequestInfo):
    id: int = Query(..., description='ID запроса на изменение типа аккаунта')
    user: UserInfo = Query(..., description='Пользователь, сделавший запрос')


class PublicProfileLinksURLS(BaseModel):

    youtube: YoutubeChannelID = Query(default=False)
    telegram: TelegramUsername = Query(default=False)
    vk: VKUsername = Query(default=False)


class PublicProfileLinks(BaseModel):
    youtube: str | None = Query(default=False,
                                description='Ссылка на канал YouTube')
    telegram: str | None = Query(default=False,
                                 description='Ссылка на канал/аккаунт в Telegram')
    vk: str | None = Query(
        default=False, description='Ссылка на страницу VK')


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
    picture: str | None = Query(default=False,
                                description='Ссылка на аватарку публичного профиля')


class PublicProfileModifiable(PublicProfileBase, PublicProfileLinksURLS, ValidateJsonWithFormBody):
    remove_picture: bool = Query(
        default=False, description='Удалить аватарку публичного профиля')
