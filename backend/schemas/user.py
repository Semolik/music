from xmlrpc.client import Boolean
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
    first_name: str | None = None
    surname: str | None = None
    is_superuser: Boolean = False
