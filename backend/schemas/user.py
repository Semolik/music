from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class UserRegister(UserAuth):
    first_name: str | None = None
    surname: str | None = None


class UserInfo(UserRegister):
    id: int
    is_superuser: bool
    is_musician: bool
    is_radio_station: bool

    class Config:
        fields = {'password': {'exclude': True}}
