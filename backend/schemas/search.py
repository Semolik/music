from typing import List
from typing import Union
from fastapi import Query
from pydantic import BaseModel

from backend.schemas.music import AlbumInfo, Track, MusicianClip
from backend.schemas.playlists import PlaylistInfo, PlaylistInfoWithoutTracks
from backend.schemas.user import PublicProfile


class SearchMusician(PublicProfile):
    ...


class SearchAlbum(AlbumInfo):
    ...


class SearchTrack(Track):
    ...


class SearchClip(MusicianClip):
    ...


class SearchPlaylist(PlaylistInfoWithoutTracks):
    ...


class AllSearchItem(BaseModel):
    type: str
    info: Union[SearchMusician, AlbumInfo,
                SearchTrack, SearchClip, SearchPlaylist]
    likes_count: int

    class Class:
        orm_mode = True
