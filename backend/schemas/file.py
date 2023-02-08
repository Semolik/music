from uuid import UUID
from pydantic import BaseModel, validator, Field
from fastapi import Query

from backend.core.config import settings
from backend.helpers.images import image_id_to_url
from backend.models.files import Image


class File(BaseModel):
    id: UUID
    user_id: int = Query(..., description="ID пользователя")
    url: str = None
    original_file_name: str = Query(
        ..., description="Имя файла, как оно было на компьютере пользователя")

    @validator("url", always=True)
    def url_generator(cls, v, values):

        return ''.join(
            [
                settings.SERVER_LINK,
                settings.API_V1_STR,
                settings.UPLOADS_ROUTE,
                settings.OTHER_FILES_ROUTE,
                str(values.get('id'))
            ]
        )

    class Config:
        orm_mode = True


class ImageLink(BaseModel):
    '''convert relationship to image link'''

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Image):
        if not v:
            return None
        if not isinstance(v, Image):
            raise TypeError('ImageLink must be Image (model)')
        return image_id_to_url(v.id)
