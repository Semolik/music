from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserRegister(UserBase, UserAuth):
    ...


class UserInfo(UserBase):
    id: int
    is_superuser: bool
    is_musician: bool
    is_radio_station: bool
