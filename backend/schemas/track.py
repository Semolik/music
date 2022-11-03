from datetime import datetime
from pydantic import BaseModel
from backend.schemas.user import PublicProfile
from backend.helpers.forms import form_body


class UploadTrack(BaseModel):
    name: str
    album_id: int
    feat: str | None = None


class Track(UploadTrack):
    id: int
    artist: PublicProfile


class CreateAlbum(BaseModel):
    name: str
    artist: PublicProfile
    date: datetime


class Album(CreateAlbum):
    id: int
    year: int
