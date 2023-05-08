from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID
from pydantic import BaseModel
from backend.schemas.music import Track
from backend.schemas.playlists_base import PlaylistInfoBase
from backend.schemas.user import UserInfo
from fastapi import Query


class order_playlist_by(str, Enum):
    created_at = 'created_at'
    name = 'name'


class PlaylistInfoWithoutTracks(PlaylistInfoBase):
    user: UserInfo = Query(
        ..., description='Пользователь, создавший плейлист')

    class Config:
        orm_mode = True


class PlaylistInfo(PlaylistInfoWithoutTracks):
    tracks: List[Track] = []

    class Config:
        orm_mode = True


class PlaylistTrack(BaseModel):
    track: Track = Query(..., description='Трек')
    playlist: PlaylistInfoWithoutTracks = Query(
        ..., description='Плейлист')

    class Config:
        orm_mode = True
