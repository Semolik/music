from typing import List
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import settings, env_config
from backend.schemas.file import File
from backend.helpers.forms import form_body


class UserUsername(BaseModel):
    username: str = Query(
        default=None,
        min_length=int(env_config.get('VITE_MIN_LOGIN_LENGTH')),
        max_length=int(env_config.get('VITE_MAX_LOGIN_LENGTH'))
    )


class UserAuth(UserUsername):
    password: str = Query(
        default=None,
        min_length=int(env_config.get('VITE_MIN_PASSWORD_LENGTH'))
    )


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserTypes(BaseModel):
    is_superuser: bool = False
    is_musician: bool = False
    is_radio_station: bool = False


class UserWithTypeRegister(UserBase, UserAuth, UserTypes):
    ...


class UserRegister(UserBase, UserAuth):
    ...


class UserModifiable(UserBase):
    ...


@form_body
class UserModifiableForm(UserBase):
    remove_picture: bool = False


class UserInfo(UserTypes, UserBase, UserUsername):
    id: int
    picture: str | None = None


@form_body
class UpdateUserRoleRequest(BaseModel):
    message: str
    account_status: str


class RoleRequestAnswer(BaseModel):
    request_id: int
    message: str | None = None
    status: str | None = None


class UpdateRoleRequestAnswer(RoleRequestAnswer):
    request_status: settings.ALLOWED_STATUSES


class ChangeRoleRequestInfo(BaseModel):
    files: List[File]
    message: str
    status: settings.ALLOWED_STATUSES
    time_created: str
    account_status: str
    answer: RoleRequestAnswer | None = None


class ChangeRoleRequestFullInfo(ChangeRoleRequestInfo):
    id: int
    user: UserInfo


class PublicProfileLinks(BaseModel):
    youtube: str | None = None
    telegram: str | None = None
    vk: str | None = None


class PublicProfileBase(BaseModel):
    name: str
    description: str | None


class PublicProfile(PublicProfileBase):
    id: int
    links: PublicProfileLinks
    picture: str | None


class MusicianFullInfo(PublicProfile):
    liked: bool


@form_body
class PublicProfileModifiable(PublicProfileBase, PublicProfileLinks):
    remove_picture: bool = False
