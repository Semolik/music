from datetime import datetime
from pydantic import BaseModel, validator
from backend.schemas.user import PublicProfile
from backend.helpers.forms import form_body
from backend.core.config import env_config


class UploadTrackBase(BaseModel):
    name: str
    album_id: int
    feat: str | None


class UploadTrack(UploadTrackBase):
    date: datetime


@form_body
class UploadTrackForm(UploadTrack):
    ...


class Track(UploadTrackBase):
    id: int
    year: int


class CreateAlbum(BaseModel):
    name: str
    date: datetime


@form_body
class CreateAlbumForm(CreateAlbum):
    ...


class AlbumBase(BaseModel):
    id: int
    name: str
    year: int


class AlbumAfterUpload(AlbumBase):
    artist_id: int


class AlbumInfo(AlbumBase):
    artist: PublicProfile
