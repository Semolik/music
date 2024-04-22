from typing import Union
from pydantic import BaseModel

from schemas.music import AlbumInfo, Track, MusicianClip
from schemas.playlists import PlaylistInfoWithoutTracks
from schemas.user import MusicianProfile


class SearchMusician(MusicianProfile):
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
    info: Union[SearchMusician, SearchAlbum,
                SearchTrack, SearchClip, SearchPlaylist]
    likes_count: int
