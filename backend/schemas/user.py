from typing import List, Tuple
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import settings, env_config
from backend.schemas.file import File
from backend.helpers.forms import ValidateJsonWithFormBody, form_body


class UserUsername(BaseModel):
    username: str = Query(
        default=None,
        min_length=int(env_config.get('VITE_MIN_LOGIN_LENGTH')),
        max_length=int(env_config.get('VITE_MAX_LOGIN_LENGTH')),
        description='Логин пользователя'
    )


class UserAuth(UserUsername):
    password: str = Query(
        default=None,
        min_length=int(env_config.get('VITE_MIN_PASSWORD_LENGTH')),
        description='Пароль пользователя'
    )


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
    type: settings.ALL_USER_ACCOUNT_STATUSES = Query(
        ..., description='Тип пользователя')


class UserWithTypeRegister(UserBase, UserAuth, UserTypes):
    ...


class UserRegister(UserBase, UserAuth):
    ...


class UserModifiable(UserBase, ValidateJsonWithFormBody):
    remove_picture: bool = Query(
        default=False,
        description='Удалить аватарку пользователя'
    )


class UserInfo(UserTypes, UserBase, UserUsername):
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


class PublicProfileLinks(BaseModel):
    youtube: str | None = Query(..., description='Ссылка на канал YouTube')
    telegram: str | None = Query(...,
                                 description='Ссылка на канал/аккаунт в Telegram')
    vk: str | None = Query(..., description='Ссылка на страницу VK')


class PublicProfileBase(BaseModel):
    name: str = Query(..., description='Оторажаемое имя')
    description: str | None = Query(..., description='Описание профиля')


class PublicProfile(PublicProfileBase):
    id: int = Query(..., description='ID публичного профиля')
    links: PublicProfileLinks = Query(..., description='Ссылки на соц. сети')
    picture: str | None = Query(...,
                                description='Ссылка на аватарку публичного профиля')


class PublicProfileModifiable(PublicProfileBase, PublicProfileLinks, ValidateJsonWithFormBody):
    remove_picture: bool = Query(
        default=False, description='Удалить аватарку публичного профиля')
