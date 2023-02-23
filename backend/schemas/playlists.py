from datetime import datetime
from typing import List, Literal
from uuid import UUID
from pydantic import BaseModel
from backend.schemas.music import Track
from backend.schemas.user import UserInfo
from fastapi import Query
from backend.core.config import env_config

order_playlist_by = Literal['created_at', 'name']


class PlaylistBase(BaseModel):
    name: str = Query(..., max_length=int(
        env_config.get('VITE_MAX_PLAYLIST_NAME_LENGTH')
    ))
    description: str = Query(..., max_length=int(
        env_config.get('VITE_MAX_PLAYLIST_DESCRIPTION_LENGTH')
    ))
    private: bool = Query(..., description='Личный плейлист или публичный')


class TracksIds(BaseModel):
    tracks_ids: List[UUID] = Query(..., description='Список id треков')


class PlaylistCreate(PlaylistBase, TracksIds):
    ...


class PlaylistInfoWithoutTracks(PlaylistBase):
    id: UUID = Query(..., description='id плейлиста')
    user: UserInfo = Query(..., description='Пользователь, создавший плейлист')
    created_at: datetime = Query(..., description='Дата создания плейлиста')

    class Config:
        orm_mode = True


class PlaylistInfo(PlaylistInfoWithoutTracks):
    tracks: List[Track] = []

    class Config:
        orm_mode = True


class PlaylistTrack(BaseModel):
    track: Track = Query(..., description='Трек')
    playlist: PlaylistInfoWithoutTracks = Query(..., description='Плейлист')
    user_id: int = Query(..., description='id пользователя')

    class Config:
        orm_mode = True
