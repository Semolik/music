from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  status, HTTPException, Query
from fastapi.responses import FileResponse
import os
from fastapi_jwt_auth import AuthJWT
from backend.db.base import CRUDBase
from backend.crud.crud_tracks import TracksCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.music import album_is_available, set_full_track_data
from backend.models.music import Album
from backend.responses import NOT_FOUND_TRACK, UNAUTHORIZED_401
from backend.schemas.music import Track
import uuid as uuid_pkg
from backend.core.config import settings
router = APIRouter(prefix="/tracks", tags=['Треки'])


@router.put('/{track_id}/like', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=bool)
def like_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
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
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение трека'''
    Authorize.jwt_optional()
    tracks_crud = TracksCrud(db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    db_album: Album = db_track.album
    current_user_id = Authorize.get_jwt_subject()
    album_is_available(album=db_album, db=db,
                       user_id=current_user_id, message="Трек не найден")
    last_listened = tracks_crud.get_last_track_listen(
        track_id=db_track.id, user_id=current_user_id)
    time = datetime.now()
    if not last_listened or not tracks_crud.track_is_started_listening(last_listened=last_listened, time=time):
        tracks_crud.create_track_listen(
            track_id=db_track.id, user_id=current_user_id, time=time)
    return set_full_track_data(track=db_track, user_id=current_user_id, db=db)


@router.get('/{track_id}/file', response_class=FileResponse)
def get_track_file(track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
                   db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """Получение трека по его id"""
    Authorize.jwt_optional()
    db_file = TracksCrud(db).get_track(track_id=track_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_album: Album = db_file.album
    current_user_id = Authorize.get_jwt_subject()
    album_is_available(album=db_album, db=db,
                       user_id=current_user_id, message="Трек не найден")
    file_path = os.path.join(settings.TRACKS_FOLDER,
                             str(track_id)+settings.SONGS_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@ router.get('/{track_id}/set-listened', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, status_code=status.HTTP_204_NO_CONTENT)
def set_listened_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Установка прослушанного трека'''
    Authorize.jwt_required()
    tracks_crud = TracksCrud(db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    current_user_id = Authorize.get_jwt_subject()
    last_track_listen = tracks_crud.get_last_track_listen(
        track_id=db_track.id, user_id=current_user_id)
    if not last_track_listen:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Прослушивание трека не найдено")
    if last_track_listen.listened:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Трек уже прослушан")
    is_listened = tracks_crud.track_is_listened(
        last_listened=last_track_listen, time=datetime.now())
    if not is_listened:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Прослушивание трека начато слишком давно или еще не закончено")
    last_track_listen.listened = True
    CRUDBase(db).update(last_track_listen)


@ router.get('/liked', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=List[Track])
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
