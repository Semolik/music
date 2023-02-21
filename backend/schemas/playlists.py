from typing import List
from uuid import UUID
from pydantic import BaseModel
from backend.schemas.music import Track
from backend.schemas.user import UserInfo


class PlaylistBase(BaseModel):
    name: str
    description: str
    private: bool


class TracksIds(BaseModel):
    tracks_ids: List[UUID]


class PlaylistCreate(PlaylistBase, TracksIds):
    ...


class PlaylistInfo(PlaylistBase):
    id: UUID
    tracks: List[Track] = []
    user: UserInfo
    private: bool

    class Config:
        orm_mode = True
