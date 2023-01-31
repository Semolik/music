from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_tracks import TracksCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.music import set_full_track_data
from backend.models.music import Album
from backend.responses import NOT_FOUND_TRACK, UNAUTHORIZED_401
from backend.schemas.music import Track
router = APIRouter(prefix="/tracks", tags=['Треки'])


@router.put('/{track_id}/like', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=bool)
def like_track(
    track_id: str = Query(..., description="ID трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Лайк трека'''
    Authorize.jwt_required()
    db_track = TracksCrud(db).get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    current_user_id = Authorize.get_jwt_subject()
    liked = TracksCrud(db).toggle_like_track(
        track_id=db_track.id, user_id=current_user_id)
    return liked


@router.get('/{track_id}', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Track)
def get_track(
    track_id: int = Query(..., description="ID трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение трека'''
    Authorize.jwt_optional()
    db_track = TracksCrud(db).get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    db_album: Album = db_track.album
    current_user_id = Authorize.get_jwt_subject()
    if db_album.open_date > datetime.now():
        if current_user_id is None or not AlbumsCruds(db).album_belongs_to_user(album=db_album, user_id=current_user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Трек не найден")
    return set_full_track_data(db_track, user_id=current_user_id)


@router.get('/liked', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=List[Track])
def get_liked_tracks(
    page: int = Query(1, description="Номер страницы"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение лайкнутых треков'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    liked_tracks = TracksCrud(db).get_liked_tracks(
        user_id=current_user_id, page=page)
    return [set_full_track_data(db=db, track=track, user_id=current_user_id) for track in liked_tracks]
