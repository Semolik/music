from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  status, HTTPException, Query
from fastapi.responses import FileResponse
import os
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import AlbumsCruds
from backend.db.base import CRUDBase
from backend.crud.crud_tracks import TracksCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import validate_authorized_user
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
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
    )
    db_track = TracksCrud(db).get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")

    liked = TracksCrud(db).toggle_like_track(
        track_id=db_track.id, user_id=db_user.id)
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
    current_user_id = None
    if not db_track or not db_track.album_uploaded:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    if not db_track.is_opened:
        db_user = validate_authorized_user(
            Authorize=Authorize, db=db,
            types=[settings.UserTypeEnum.musician]
        )
        if not AlbumsCruds(db).album_belongs_to_user(album=db_track.album, user_id=db_user.id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Трек не найден")
        current_user_id = db_user.id
    else:
        current_user_id = Authorize.get_jwt_subject()
    return set_full_track_data(track=db_track, user_id=current_user_id, db=db)


@router.post('/{track_id}/listening', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, status_code=status.HTTP_204_NO_CONTENT)
def start_listening_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Начало прослушивания трека'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
    )
    tracks_crud = TracksCrud(db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    last_listened = tracks_crud.get_last_track_listen(
        track_id=db_track.id, user_id=db_user.id)
    time = datetime.now()
    if not last_listened or not tracks_crud.track_is_started_listening(last_listened=last_listened, time=time):
        tracks_crud.create_track_listen(
            track_id=db_track.id, user_id=db_user.id, time=time)


@router.put('/{track_id}/listening', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, status_code=status.HTTP_204_NO_CONTENT)
def set_listened_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Установка прослушанного трека'''
    Authorize.jwt_required()

    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
    )
    tracks_crud = TracksCrud(db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    last_track_listen = tracks_crud.get_last_track_listen(
        track_id=db_track.id, user_id=db_user.id)
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


@router.get('/{track_id}/file', response_class=FileResponse)
def get_track_file(track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
                   db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """Получение трека по его id"""
    Authorize.jwt_optional()
    db_track = TracksCrud(db).get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Трек не найден")
    if not db_track.is_opened:
        db_user = validate_authorized_user(
            Authorize=Authorize, db=db, types=[settings.UserTypeEnum.musician]
        )
        album: Album = db_track.album
        if db_user != album.musician_user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Трек не найден")
    file_path = os.path.join(settings.TRACKS_FOLDER,
                             str(track_id)+settings.SONGS_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/liked', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=List[Track])
def get_liked_tracks(
    page: int = Query(1, description="Номер страницы"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение лайкнутых треков'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize,
        db=db
    )
    user_id = db_user.id
    liked_tracks = TracksCrud(db).get_liked_tracks(
        user_id=user_id,
        page=page
    )
    return [set_full_track_data(db=db, track=track, user_id=user_id) for track in liked_tracks if track.is_available]
