from typing import List
from pydantic import BaseModel

from backend.schemas.music import AlbumInfo, AlbumTrack, MusicianClip
from backend.schemas.user import PublicProfile


class SearchMusician(PublicProfile):
    ...


class SearchAlbum(AlbumInfo):
    ...


class SearchTrack(AlbumTrack):
    ...


class SearchClip(MusicianClip):
    ...


class AllSearch(BaseModel):
    albums: List[SearchAlbum] = []
    tracks: List[SearchTrack] = []
    musicians: List[SearchMusician] = []
    clips: List[SearchClip] = []
