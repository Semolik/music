import uuid as uuid_pkg
from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import Query, Form
from backend.schemas.user import PublicProfile
from backend.helpers.forms import form_body
from backend.core.config import env_config


class CreateAlbum(BaseModel):
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_ALBUM_NAME_LENGTH'))
    )
    date: datetime
    genres_ids: List[int] | None = None


class UpdateAlbum(CreateAlbum):
    id: int
    tracks_ids: List[uuid_pkg.UUID]


@form_body
class UpdateAlbumForm(UpdateAlbum):
    ...


@form_body
class CreateAlbumForm(CreateAlbum):
    ...


class CreateGenre(BaseModel):
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_GENRE_NAME_LENGTH'))
    )


@form_body
class CreateGenreForm(CreateGenre):
    ...


class UpdateGenre(CreateGenre):
    id: int


@form_body
class UpdateGenreForm(UpdateGenre):
    ...


class Genre(UpdateGenre):
    picture: str


class AlbumBase(BaseModel):
    id: int
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_ALBUM_NAME_LENGTH'))
    )
    year: int
    genres: List[Genre]


class AlbumAfterUpload(AlbumBase):
    musician_id: int


class AlbumIsCLosed(BaseModel):
    closed_uploading: bool


class UploadTrackBase(BaseModel):
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_TRACK_NAME_LENGTH'))
    )
    album_id: int
    feat: str | None = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_TRACK_FEAT_LENGTH'))
    )


@form_body
class UploadTrackForm(UploadTrackBase):
    ...


class TrackAfterUpload(UploadTrackBase):
    id: uuid_pkg.UUID
    picture: str | None = None


class AlbumTrack(TrackAfterUpload):
    duration: float
    url: str
    liked: bool = False


class AlbumInfo(AlbumBase):
    musician: PublicProfile
    picture: str | None
    date: datetime


class AlbumWithTracks(AlbumInfo):
    tracks: List[AlbumTrack]
    date: datetime | None = None


class Track(AlbumTrack):
    album: AlbumInfo


class Liked(BaseModel):
    liked: bool


class CreateMusicianClip(BaseModel):

    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_CLIP_NAME_LENGTH'))
    )
    video_id: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_YOUTUBE_VIDEOID_LENGTH'))
    )


@form_body
class CreateMusicianClipForm(CreateMusicianClip):
    image_from_youtube: bool


@form_body
class UpdateMusicianClipForm(CreateMusicianClipForm):
    id: int


class MusicianClip(BaseModel):
    id: int
    musician_id: int
    name: str
    video: str
    video_id: str
    picture: str


class MusicianFullInfo(PublicProfile):
    liked: bool
    clips: List[MusicianClip]
