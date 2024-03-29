from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import Query
import uuid

from backend.schemas.music import Genre, GenreWithoutLiked


class UsersStats(BaseModel):
    user_count: int = Query(..., description="Количество пользователей")
    admin_count: int = Query(..., description="Количество администраторов")
    change_role_request_count: int = Query(
        ..., description="Количество запросов на смену типа аккаунта")
    musician_count: int = Query(..., description="Количество музыкантов")


class StatsDay(BaseModel):
    day: datetime = Query(..., description="Дата")
    listens: int = Query(..., description="Количество прослушиваний")


class StatsBase(BaseModel):
    total_listens: int = Query(...,
                               description="Общее количество прослушиваний")
    calendar: List[StatsDay] = Query(...,
                                     description="Статистика по дням")


class TrackStats(StatsBase):
    track_id: uuid.UUID = Query(..., description="ID трека")


class AlbumStats(StatsBase):
    album_id: int = Query(..., description="ID альбома")


class MusicianStats(StatsBase):
    musician_id: int = Query(..., description="ID музыканта")


class GenreStats(GenreWithoutLiked):
    album_count: int = Query(default=0, description="Количество альбомов")

    class Config:
        orm_mode = True
