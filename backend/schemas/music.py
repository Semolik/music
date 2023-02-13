import uuid as uuid_pkg
from datetime import datetime
from typing import List
from pydantic import BaseModel,  validator
from fastapi import Query
from backend.schemas.file import ImageLink
from backend.schemas.links import YoutubeVideoIdToUrl
from backend.schemas.user import PublicProfile
from backend.helpers.forms import form_body
from backend.core.config import env_config
from backend.helpers.forms import ValidateJsonWithFormBody


class CreateAlbumBase(ValidateJsonWithFormBody):
    name: str = Query(
        default=None,
        max_length=int(env_config.get('VITE_MAX_ALBUM_NAME_LENGTH')),
        min_length=1
    )
    open_date: datetime = Query(..., description="Дата создания альбома")


class CreateAlbum(CreateAlbumBase):

    genres_ids: List[int] | None = Query([], description="Список ID жанров")


class UpdateAlbum(CreateAlbum):
    tracks_ids: List[uuid_pkg.UUID] = Query(...,
                                            description="Список ID треков")


@form_body
class CreateAlbumForm(CreateAlbum):
    ...


class GenreBase(BaseModel):
    name: str = Query(
        ...,
        max_length=int(env_config.get('VITE_MAX_GENRE_NAME_LENGTH')),
        min_length=1,
        description="Название жанра"
    )


@form_body
class GenreBaseForm(GenreBase):
    ...


class Genre(GenreBase):
    id: int = Query(..., description="ID жанра")
    picture: ImageLink = Query(..., description="Ссылка на картинку жанра")

    class Config:
        orm_mode = True


class AlbumBase(CreateAlbumBase):
    id: int
    year: int = Query(None, description="Год выпуска альбома")
    genres: List[Genre] = Query(..., description="Список жанров альбома")

    class Config:
        orm_mode = True


class AlbumAfterUpload(AlbumBase):
    musician_id: int = Query(..., description="ID музыканта")


class AlbumIsCLosed(BaseModel):
    closed_uploading: bool = Query(...,
                                   description="Закрыто ли добавление треков")


class UploadTrackBase(BaseModel):
    name: str = Query(
        ...,
        max_length=int(env_config.get('VITE_MAX_TRACK_NAME_LENGTH')),
        min_length=int(env_config.get('VITE_MIN_TRACK_NAME_LENGTH')),
        description="Название трека"
    )
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


class AlbumInfoWithoutMusician(AlbumBase):
    picture: ImageLink = Query(...,
                               description="Ссылка на картинку альбома")


class AlbumInfo(AlbumInfoWithoutMusician):
    musician: PublicProfile = Query(..., description="Информация о музыканте")

    class Config:
        orm_mode = True


class AlbumWithTracks(AlbumInfo):
    tracks: List[AlbumTrack] = Query(..., description="Список треков альбома")


class Track(AlbumTrack):
    album: AlbumInfo = Query(..., description="Информация об альбоме")


class CreateMusicianClip(BaseModel):

    name: str = Query(
        ...,
        max_length=int(env_config.get('VITE_MAX_CLIP_NAME_LENGTH')),
        description="Название клипа"
    )
    video_id: str = Query(
        ...,
        max_length=int(env_config.get('VITE_MAX_YOUTUBE_VIDEOID_LENGTH')),
        description="ID видео на YouTube"
    )


@form_body
class CreateMusicianClipForm(CreateMusicianClip):
    image_from_youtube: bool = Query(...,
                                     description="Использовать ли картинку с YouTube")


class MusicianClipWithoutMusician(CreateMusicianClip):
    id: int = Query(..., description="ID клипа")
    picture: ImageLink = Query(..., description="Ссылка на картинку клипа")

    video_id: str = Query(..., description="ID видео на YouTube")
    video: str = None

    @validator("video", always=True)
    def link_from_video_id(cls, v, values):

        video_id = values.get("video_id")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return v

    class Config:
        orm_mode = True


class MusicianClip(MusicianClipWithoutMusician):
    musician_id: int = Query(..., description="ID музыканта")

    class Config:
        orm_mode = True


class MusicianInfo(PublicProfile):
    liked: bool = Query(default=False, description="Лайкнут ли музыкант")


class MusicianFullInfo(MusicianInfo):

    clips: List[MusicianClipWithoutMusician] = Query(...,
                                                     description="Клипы музыканта")
    albums: List[AlbumInfoWithoutMusician] = Query(...,
                                                   description="Альбомы музыканта")

    class Config:
        orm_mode = True
