from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

from fastapi import Query
from backend.core.config import env_config
from backend.schemas.file import ImageLink


class PlaylistBase(BaseModel):
    name: str = Query(..., max_length=int(
        env_config.get('VITE_MAX_PLAYLIST_NAME_LENGTH')
    ), description='Название плейлиста', min_length=1)
    description: str = Query(None, max_length=int(
        env_config.get('VITE_MAX_PLAYLIST_DESCRIPTION_LENGTH')
    ))
    private: bool = Query(...,
                          description='Личный плейлист или публичный')


class TracksIds(BaseModel):
    tracks_ids: List[UUID] = Query(...,
                                   description='Список id треков')


class PlaylistCreate(PlaylistBase, TracksIds):
    ...


class PlaylistInfoBase(PlaylistBase):
    id: UUID = Query(..., description='id плейлиста')
    created_at: datetime = Query(...,
                                 description='Дата создания плейлиста')
    picture: ImageLink = None
    tracks_count: int = Query(
        ..., description='Количество треков в плейлисте')
    liked: bool = Query(
        default=False, description='Понравился ли плейлист пользователю')

    class Config:
        orm_mode = True
