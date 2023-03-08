from typing import List
from fastapi import Depends, APIRouter, status, HTTPException, Query
from backend.crud.crud_musician import MusicianCrud
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_playlists import PlaylistsCrud
from backend.crud.crud_clips import ClipsCruds
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_search import SearchCrud
from backend.schemas.search import AllSearchItem, SearchMusician, SearchAlbum, SearchPlaylist, SearchTrack, SearchClip
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import Authenticate
from backend.core.config import settings
from fastapi_jwt_auth import AuthJWT
router = APIRouter(tags=['Поиск'], prefix='/search')


@router.get('/autocomplete', response_model=List[AllSearchItem])
def search(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    return SearchCrud(Auth.db).search_all_by_name_sorted_by_likes(name=text, user_id=Auth.current_user_id)


@router.get('/musician', response_model=List[SearchMusician])
def search_musician(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):

    search_crud = SearchCrud(Auth.db)
    db_musicians = search_crud.search_musicians_by_name(
        name=text, limit=settings.SEARCH_MUSICIAN_LIMIT)
    db_musicians_objs = []
    for musician in db_musicians:
        musician_obj = SearchMusician.from_orm(musician)
        if Auth.current_user_id:
            musician_obj.liked = MusicianCrud(Auth.db).musician_is_liked(
                musician_id=musician.id, user_id=Auth.current_user_id)
        db_musicians_objs.append(musician_obj)
    return db_musicians_objs


@router.get('/album', response_model=List[SearchAlbum])
def search_album(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):

    search_crud = SearchCrud(Auth.db)
    db_albums = search_crud.search_albums_by_name(
        name=text, limit=settings.SEARCH_ALBUM_LIMIT)
    db_albums_objs = []
    for album in db_albums:
        album_obj = SearchAlbum.from_orm(album)
        if Auth.current_user_id:
            album_obj.liked = AlbumsCruds(Auth.db).album_is_liked(
                album_id=album.id, user_id=Auth.current_user_id)
        db_albums_objs.append(album_obj)
    return db_albums_objs


@router.get('/track', response_model=List[SearchTrack])
def search_track(text: str = Query(description="Поисковый запрос"),  Auth: Authenticate = Depends(Authenticate(required=False))):

    search_crud = SearchCrud(Auth.db)
    db_tracks = search_crud.search_tracks_by_name(
        name=text, limit=settings.SEARCH_TRACK_LIMIT)
    db_tracks_objs = []
    for track in db_tracks:
        track_obj = SearchTrack.from_orm(track)
        if Auth.current_user_id:
            track_obj.liked = TracksCrud(Auth.db).track_is_liked(
                track_id=track.id, user_id=Auth.current_user_id)
        db_tracks_objs.append(track_obj)
    return db_tracks_objs


@router.get('/clip', response_model=List[SearchClip])
def search_clip(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    search_crud = SearchCrud(db)
    db_clips = search_crud.search_clips_by_name(
        name=text, limit=settings.SEARCH_CLIP_LIMIT)
    return db_clips


@router.get('/playlist', response_model=List[SearchPlaylist])
def search_playlist(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    search_crud = SearchCrud(Auth.db)
    db_playlists = search_crud.search_playlists_by_name(
        name=text, limit=settings.SEARCH_PLAYLIST_LIMIT, current_user=Auth.current_user)
    # db_playlists_objs = []
    # for playlist in db_playlists:
    #     playlist_obj = SearchPlaylist.from_orm(playlist)
    #     if Auth.current_user_id:
    #         playlist_obj.liked = PlaylistsCrud(Auth.db).playlist_is_liked(
    #             playlist_id=playlist.id, user_id=Auth.current_user_id)
    #     db_playlists_objs.append(playlist_obj)
    return db_playlists
