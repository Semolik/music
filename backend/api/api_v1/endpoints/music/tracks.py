from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, APIRouter,  status, HTTPException, Query
from fastapi.responses import FileResponse
import os
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_user import UserCruds
from backend.db.base import CRUDBase
from backend.crud.crud_tracks import TracksCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import Authenticate
from backend.helpers.music import set_full_track_data
from backend.models.albums import Album
from backend.responses import NOT_FOUND_TRACK, UNAUTHORIZED_401
from backend.schemas.music import Track
import uuid as uuid_pkg
from backend.core.config import settings
from backend.schemas.statistics import TrackStats
router = APIRouter(prefix="/tracks", tags=['Треки'])


@router.put('/{track_id}/like', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=bool)
def like_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Лайк трека'''

    db_track = TracksCrud(Auth.db).get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")

    liked = TracksCrud(Auth.db).toggle_like_track(
        track_id=db_track.id, user_id=Auth.current_user_id)
    return liked


@router.get('/liked', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=List[Track])
def get_liked_tracks(
    page: int = Query(1, description="Номер страницы"),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение лайкнутых треков'''

    liked_tracks = TracksCrud(Auth.db).get_liked_tracks(
        user_id=Auth.current_user_id,
        page=page
    )
    return liked_tracks


@router.get('/popular', response_model=List[Track])
def get_popular_tracks(
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение популярных треков'''

    popular_tracks = TracksCrud(Auth.db).get_popular_tracks()
    return popular_tracks


@router.get('/popular/month', response_model=List[Track])
def get_popular_tracks_month(
    Auth: Authenticate = Depends(Authenticate(required=False)),
    page_size: int = Query(settings.POPULAR_TRACKS_LIMIT,
                           description="Размер страницы", ge=1, le=settings.POPULAR_TRACKS_LIMIT),
    page: int = Query(1, description="Номер страницы"),
):
    '''Получение популярных треков за месяц'''

    popular_tracks = TracksCrud(Auth.db).get_popular_tracks(
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        page=page,
        page_size=page_size
    )
    return popular_tracks


@router.get('/{track_id}', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Track)
def get_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение трека'''

    tracks_crud = TracksCrud(Auth.db)
    db_track = tracks_crud.get_track(track_id=track_id)

    if not db_track or not db_track.album_uploaded:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    if not db_track.is_opened:
        if not Auth.current_user or AlbumsCruds(Auth.db).album_belongs_to_user(album=db_track.album, user_id=Auth.current_user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Трек не найден")
    track_obj = Track.from_orm(db_track)
    if Auth.current_user_id:
        track_obj.liked = tracks_crud.track_is_liked(
            track_id=db_track.id, user_id=Auth.current_user_id)
    return track_obj


@router.get('/{track_id}/stats', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=TrackStats)
def get_track_statistics(track_id: uuid_pkg.UUID, Auth: Authenticate = Depends(Authenticate(is_admin=True, is_musician=True))):
    '''Получение статистики по треку'''
    tracks_crud = TracksCrud(db=Auth.db)
    track = tracks_crud.get_track(track_id=track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Трек не найден'
        )
    users_cruds = UserCruds(db=Auth.db)
    db_public_profile = users_cruds.get_public_profile_by_id(
        Auth.current_user_id)
    if not (Auth.current_user.type == settings.UserTypeEnum.superuser) and not (db_public_profile or db_public_profile.id != track.artist_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет доступа к этой информации'
        )

    return tracks_crud.get_track_statistics(track=track)


@router.post('/{track_id}/listening', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, status_code=status.HTTP_204_NO_CONTENT)
def start_listening_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Начало прослушивания трека'''

    tracks_crud = TracksCrud(Auth.db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    last_listened = tracks_crud.get_last_track_listen(
        track_id=db_track.id, user_id=Auth.current_user_id)
    time = datetime.now()
    if not last_listened or not tracks_crud.track_is_started_listening(last_listened=last_listened, time=time):
        tracks_crud.create_track_listen(
            track_id=db_track.id, user_id=Auth.current_user_id, time=time)


@router.put('/{track_id}/listening', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, status_code=status.HTTP_204_NO_CONTENT)
def set_listened_track(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Установка прослушанного трека'''

    tracks_crud = TracksCrud(Auth.db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    last_track_listen = tracks_crud.get_last_track_listen(
        track_id=db_track.id, user_id=Auth.current_user_id)
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
    tracks_crud.update(last_track_listen)


@router.get('/{track_id}/file', response_class=FileResponse)
def get_track_file(
    track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    """Получение трека по его id"""

    db_track = TracksCrud(Auth.db).get_track(track_id=track_id)
    if not db_track or not db_track.is_available:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Трек не найден")
    if not db_track.is_opened:
        album: Album = db_track.album
        if not Auth.current_user or not AlbumsCruds(Auth.db).album_belongs_to_user(album=album, user_id=Auth.current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Трек не найден")
    file_path = os.path.join(settings.TRACKS_FOLDER,
                             str(track_id)+settings.SONGS_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")
