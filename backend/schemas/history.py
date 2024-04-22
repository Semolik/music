from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Union
from schemas.music import AlbumInfo, Track
from schemas.playlists import PlaylistInfoWithoutTracks
from schemas.user import MusicianProfile


class HistoryItem(BaseModel):
    id: UUID
    type: str
    info: Union[AlbumInfo, PlaylistInfoWithoutTracks, MusicianProfile]

    class Config:
        orm_mode = True


class HistoryBase(BaseModel):
    id: UUID
    listen_datetime: datetime

    class Config:
        orm_mode = True


class HistoryTrack(HistoryBase):
    track: Track

    class Config:
        orm_mode = True


class HistoryPlaylist(HistoryBase):
    playlist: PlaylistInfoWithoutTracks

    class Config:
        orm_mode = True


class HistoryAlbum(HistoryBase):
    album: AlbumInfo

    class Config:
        orm_mode = True


class HistoryMusician(HistoryBase):
    musician: MusicianProfile

    class Config:
        orm_mode = True
