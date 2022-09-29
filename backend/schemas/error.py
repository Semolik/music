
from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class HTTP_401_UNAUTHORIZED(BaseModel):
    detail: str = "неправильное имя пользователя или пароль"
