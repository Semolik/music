from typing import List
from pydantic import BaseModel

from backend.schemas.music import AlbumInfo, AlbumTrack, MusicianClip
from backend.schemas.user import PublicProfile


class AllSearch(BaseModel):
    albums: List[AlbumInfo]
    tracks: List[AlbumTrack]
    musicians: List[PublicProfile]
    clips: List[MusicianClip]
