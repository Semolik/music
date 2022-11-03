from datetime import datetime
from pydantic import BaseModel, validator
from backend.schemas.user import PublicProfile
from backend.helpers.forms import form_body
from backend.core.config import env_config


class Date(BaseModel):
    birthdate: datetime

    @validator("birthdate", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            env_config.get('VITE_DATE_FORMAT')
        ).date()


class UploadTrack(BaseModel):
    name: str
    album_id: int
    feat: str | None = None


class Track(UploadTrack):
    id: int


class CreateAlbum(BaseModel):
    name: str
    date: datetime


@form_body
class CreateAlbumForm(CreateAlbum):
    ...


class Album(BaseModel):
    id: int
    name: str
    year: int
    artist: PublicProfile
