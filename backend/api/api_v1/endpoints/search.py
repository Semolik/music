from typing import List
from fastapi import Depends, APIRouter,  Query
from backend.crud.crud_genres import GenresCruds
from backend.crud.crud_musician import MusicianCrud
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_playlists import PlaylistsCrud
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_search import SearchCrud
from backend.schemas.music import Genre
from backend.schemas.search import AllSearchItem, SearchMusician, SearchAlbum, SearchPlaylist, SearchTrack, SearchClip
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import Authenticate
from backend.core.config import settings

router = APIRouter(tags=['Поиск'], prefix='/search')


@router.get('/autocomplete', response_model=List[AllSearchItem])
def search(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Поиск по всему'''
    return SearchCrud(Auth.db).search_all_by_name_sorted_by_likes(name=text, user_id=Auth.current_user_id)


@router.get('/musician', response_model=List[SearchMusician])
def search_musician(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Поиск по музыкантам'''
    search_crud = SearchCrud(Auth.db)
    db_musicians = search_crud.search_musicians_by_name(
        name=text, limit=settings.SEARCH_MUSICIAN_LIMIT)
    if Auth.current_user_id:
        for musician in db_musicians:
            musician.current_user_id = Auth.current_user_id
    return db_musicians


@router.get('/album', response_model=List[SearchAlbum])
def search_album(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Поиск по альбомам'''
    search_crud = SearchCrud(Auth.db)
    db_albums = search_crud.search_albums_by_name(
        name=text, limit=settings.SEARCH_ALBUM_LIMIT)
    if Auth.current_user_id:
        for album in db_albums:
            album.current_user_id = Auth.current_user_id
    return db_albums


@router.get('/track', response_model=List[SearchTrack])
def search_track(text: str = Query(description="Поисковый запрос"),  Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Поиск по трекам'''
    search_crud = SearchCrud(Auth.db)
    db_tracks = search_crud.search_tracks_by_name(
        name=text, limit=settings.SEARCH_TRACK_LIMIT)
    if Auth.current_user_id:
        for track in db_tracks:
            track.current_user_id = Auth.current_user_id
    return db_tracks


@router.get('/clip', response_model=List[SearchClip])
def search_clip(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    '''Поиск по клипам'''
    search_crud = SearchCrud(db)
    db_clips = search_crud.search_clips_by_name(
        name=text, limit=settings.SEARCH_CLIP_LIMIT)
    return db_clips


@router.get('/playlist', response_model=List[SearchPlaylist])
def search_playlist(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Поиск по плейлистам'''
    search_crud = SearchCrud(Auth.db)
    db_playlists = search_crud.search_playlists_by_name(
        name=text, limit=settings.SEARCH_PLAYLIST_LIMIT)
    if Auth.current_user_id:
        for playlist in db_playlists:
            playlist.current_user_id = Auth.current_user_id
    return db_playlists


@router.get('/genres', response_model=List[Genre])
def get_genres(text: str = Query(description="Поисковый запрос"), Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Поиск по жанрам'''
    search_crud = SearchCrud(Auth.db)
    db_genres = search_crud.search_genres_by_name_sorted_by_likes(
        name=text, limit=settings.SEARCH_GENRE_LIMIT)
    if Auth.current_user_id:
        for genre in db_genres:
            genre.current_user_id = Auth.current_user_id
    return db_genres
