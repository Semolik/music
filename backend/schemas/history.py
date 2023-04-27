from pydantic import BaseModel
from typing import Union
from backend.schemas.music import AlbumInfo
from backend.schemas.playlists import PlaylistInfoWithoutTracks
from backend.schemas.user import MusicianProfile


class HistoryItem(BaseModel):
    id: int
    type: str
    info: Union[AlbumInfo, PlaylistInfoWithoutTracks, MusicianProfile]

    class Config:
        orm_mode = True
