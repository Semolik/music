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
    date: datetime = Query(..., description="Дата создания альбома")
    genres_ids: List[int] | None = Query([], description="Список ID жанров")


class UpdateAlbum(CreateAlbum):
    id: int = Query(..., description="ID альбома")
    tracks_ids: List[uuid_pkg.UUID] = Query(...,
                                            description="Список ID треков")


@form_body
class UpdateAlbumForm(UpdateAlbum):
    ...


@form_body
class CreateAlbumForm(CreateAlbum):
    ...


class CreateGenre(BaseModel):
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_GENRE_NAME_LENGTH')),
        description="Название жанра"
    )


@form_body
class CreateGenreForm(CreateGenre):
    ...


class UpdateGenre(CreateGenre):
    id: int = Query(..., description="ID жанра")


@form_body
class UpdateGenreForm(UpdateGenre):
    ...


class Genre(UpdateGenre):
    picture: str = Query(..., description="Ссылка на картинку жанра")


class AlbumBase(BaseModel):
    id: int
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_ALBUM_NAME_LENGTH')),
        description="Название альбома"
    )
    year: int = Query(..., description="Год выпуска альбома")
    genres: List[Genre] = Query(..., description="Список жанров альбома")


class AlbumAfterUpload(AlbumBase):
    musician_id: int = Query(..., description="ID музыканта")


class AlbumIsCLosed(BaseModel):
    closed_uploading: bool = Query(...,
                                   description="Закрыто ли добавление треков")


class UploadTrackBase(BaseModel):
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_TRACK_NAME_LENGTH')),
        description="Название трека"
    )
    album_id: int = Query(..., description="ID альбома")
    feat: str | None = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_TRACK_FEAT_LENGTH')),
        description="Участники трека"
    )


@form_body
class UploadTrackForm(UploadTrackBase):
    ...


class TrackAfterUpload(UploadTrackBase):
    id: uuid_pkg.UUID = Query(..., description="ID трека")
    picture: str | None = Query(..., description="Ссылка на картинку трека")


class AlbumTrack(TrackAfterUpload):
    duration: float = Query(..., description="Длительность трека")
    url: str = Query(..., description="Ссылка на трек")
    liked: bool = Query(..., description="Лайкнут ли трек")


class AlbumInfo(AlbumBase):
    musician: PublicProfile = Query(..., description="Информация о музыканте")
    picture: str | None = Query(..., description="Ссылка на картинку альбома")
    date: datetime = Query(..., description="Дата создания альбома")


class AlbumWithTracks(AlbumInfo):
    tracks: List[AlbumTrack] = Query(..., description="Список треков альбома")
    date: datetime | None = Query(..., description="Дата создания альбома")


class Track(AlbumTrack):
    album: AlbumInfo = Query(..., description="Информация об альбоме")


class Liked(BaseModel):
    liked: bool


class CreateMusicianClip(BaseModel):

    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_CLIP_NAME_LENGTH')),
        description="Название клипа"
    )
    video_id: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_YOUTUBE_VIDEOID_LENGTH')),
        description="ID видео на YouTube"
    )


@form_body
class CreateMusicianClipForm(CreateMusicianClip):
    image_from_youtube: bool = Query(...,
                                     description="Использовать ли картинку с YouTube")


@form_body
class UpdateMusicianClipForm(CreateMusicianClipForm):
    id: int = Query(..., description="ID клипа")


class MusicianClip(BaseModel):
    id: int = Query(..., description="ID клипа")
    musician_id: int = Query(..., description="ID музыканта")
    name: str = Query(..., description="Название клипа")
    video: str = Query(..., description="Ссылка на видео на YouTube")
    video_id: str = Query(..., description="ID видео на YouTube")
    picture: str = Query(..., description="Ссылка на картинку клипа")


class MusicianFullInfo(PublicProfile):
    liked: bool | None = Query(..., description="Лайкнут ли музыкант")
    clips: List[MusicianClip] = Query(...,
                                      description="Список клипов музыканта")
    albums: List[AlbumInfo] = Query(...,
                                    description="Список альбомов музыканта")
