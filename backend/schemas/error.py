
from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class HTTP_401_UNAUTHORIZED(BaseModel):
    detail: str = "неправильное имя пользователя или пароль"


class USER_NOT_FOUND(BaseModel):
    detail: str = "Пользователь не найден"


class ALBUM_NOT_FOUND(BaseModel):
    detail: str = "Альбом не найден"


class NOT_ENOUGH_RIGHTS_403(BaseModel):
    detail: str = "Недостаточно прав"


class GENRE_IS_NOT_UNIQUE(BaseModel):
    detail: str = "Название жанра должно быть уникальным"
