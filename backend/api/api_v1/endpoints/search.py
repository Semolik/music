from typing import List
from fastapi import Depends, APIRouter, status, HTTPException, Query
from backend.crud.crud_search import SearchCrud
from backend.schemas.search import AllSearch, SearchMusician, SearchAlbum, SearchTrack, SearchClip
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import validate_authorized_user
from backend.core.config import settings
router = APIRouter(tags=['Поиск'], prefix='/search')


@router.get('/autocomplete', response_model=AllSearch)
def search(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    search_crud = SearchCrud(db)
    db_albums = search_crud.search_albums_by_name(name=text)
    db_tracks = search_crud.search_tracks_by_name(name=text)
    db_musicians = search_crud.search_musicians_by_name(name=text)
    db_clips = search_crud.search_clips_by_name(name=text)

    return AllSearch(
        albums=db_albums,
        tracks=db_tracks,
        musicians=db_musicians,
        clips=db_clips
    )


@router.get('/musician', response_model=List[SearchMusician])
def search_musician(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    search_crud = SearchCrud(db)
    db_musicians = search_crud.search_musicians_by_name(
        name=text, limit=settings.SEARCH_MUSICIAN_LIMIT)
    return db_musicians


@router.get('album', response_model=List[SearchAlbum])
def search_album(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    search_crud = SearchCrud(db)
    db_albums = search_crud.search_albums_by_name(
        name=text, limit=settings.SEARCH_ALBUM_LIMIT)
    return db_albums


@router.get('/track', response_model=List[SearchTrack])
def search_track(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    search_crud = SearchCrud(db)
    db_tracks = search_crud.search_tracks_by_name(
        name=text, limit=settings.SEARCH_TRACK_LIMIT)
    return db_tracks


@router.get('/clip', response_model=List[SearchClip])
def search_clip(text: str = Query(description="Поисковый запрос"), db: Session = Depends(get_db)):
    search_crud = SearchCrud(db)
    db_clips = search_crud.search_clips_by_name(
        name=text, limit=settings.SEARCH_CLIP_LIMIT)
    return db_clips
