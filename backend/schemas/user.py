from typing import List
from pydantic import BaseModel
from core.config import settings
from schemas.file import File
from helpers.forms import form_body


class UserAuth(BaseModel):
    username: str
    password: str


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
    ...
    remove_picture: bool = False


class UserInfo(UserTypes, UserBase):
    id: int
    username: str
    picture: str | None = None


@form_body
class UpdateUserRoleRequest(BaseModel):
    message: str
    account_status: str


class UpdateRoleRequestAnswer(BaseModel):
    request_id: int
    message: str | None = None
    request_status: settings.ALLOWED_STATUSES
    status: str | None = None


class ChangeRoleRequestInfo(BaseModel):
    files: List[File]
    message: str
    status: settings.ALLOWED_STATUSES
    time_created: str
    account_status: str


class ChangeRoleRequestFullInfo(ChangeRoleRequestInfo):
    id: int
    user: UserInfo
