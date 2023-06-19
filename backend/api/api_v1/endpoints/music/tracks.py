from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, APIRouter, File, Path, UploadFile,  status, HTTPException, Query
from fastapi.responses import FileResponse
import os
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_user import UserCruds
from backend.crud.crud_tracks import TracksCrud
from backend.helpers.auth_helper import Authenticate
from backend.helpers.images import save_image
from backend.helpers.music import update_track
from backend.models.albums import Album
from backend.schemas.music import Track, UploadTrackForm
import uuid as uuid_pkg
from backend.core.config import settings
from backend.schemas.playlists import PlaylistInfoWithoutTracks
from backend.schemas.statistics import TrackStats
router = APIRouter(prefix="/tracks", tags=['Треки'])


@router.put('/{track_id}/like',  response_model=bool)
def like_track(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
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


@router.get('/liked',  response_model=List[Track])
def get_liked_tracks(
    page: int = Query(1, description="Номер страницы"),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение лайкнутых треков'''

    liked_tracks = TracksCrud(Auth.db).get_liked_tracks(
        user_id=Auth.current_user_id,
        page=page
    )
    for track in liked_tracks:
        track.is_liked = True
    return liked_tracks


@router.get('/popular', response_model=List[Track])
def get_popular_tracks(
    Auth: Authenticate = Depends(Authenticate(required=False)),
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(settings.POPULAR_TRACKS_LIMIT,
                           description="Размер страницы", ge=1, le=settings.POPULAR_TRACKS_LIMIT),
):
    '''Получение популярных треков'''
    popular_tracks = TracksCrud(Auth.db).get_popular_tracks(
        page=page,
        page_size=page_size
    )
    for track in popular_tracks:
        track.current_user_id = Auth.current_user_id
    return popular_tracks


@router.get('/popular/period', response_model=List[Track])
def get_popular_tracks_period(
    Auth: Authenticate = Depends(Authenticate(required=False)),
    page_size: int = Query(settings.POPULAR_TRACKS_LIMIT,
                           description="Размер страницы", ge=1, le=settings.POPULAR_TRACKS_LIMIT),
    page: int = Query(1, description="Номер страницы"),
    start_date: datetime = Query(..., description="Дата начала периода"),
    end_date: datetime = Query(..., description="Дата конца периода"),
):
    '''Получение популярных треков за месяц'''

    popular_tracks = TracksCrud(Auth.db).get_popular_tracks(
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )
    for track in popular_tracks:
        track.current_user_id = Auth.current_user_id
    return popular_tracks


@router.get('/{track_id}',  response_model=Track)
def get_track(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
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
    db_track.current_user_id = Auth.current_user_id
    return db_track


@router.put('/{track_id}', response_model=Track)
def update_track_by_id(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
    trackData: UploadTrackForm = Depends(UploadTrackForm),
    trackPicture: UploadFile = File(None, description="Изображение трека"),
    track: UploadFile = File(None, description="Файл трека"),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Обновление трека'''
    tracks_crud = TracksCrud(Auth.db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    if not AlbumsCruds(Auth.db).album_belongs_to_user(album=db_track.album, user_id=Auth.current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет доступа к этому треку")
    if db_track.album.uploaded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя изменить трек, из уже загруженного альбома")
    db_image = save_image(
        db=Auth.db,
        upload_file=trackPicture,
        user_id=Auth.current_user_id,
    ) if trackPicture else None
    db_track = update_track(
        db=Auth.db,
        track=db_track,
        track_form=trackData,
        picture=db_image,
        upload_file=track
    )
    return db_track


@router.delete('/{track_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_track(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Удаление трека'''
    tracks_crud = TracksCrud(Auth.db)
    db_track = tracks_crud.get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    if not AlbumsCruds(Auth.db).album_belongs_to_user(album=db_track.album, user_id=Auth.current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет доступа к этому треку")
    if db_track.album.uploaded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить трек, из уже загруженного альбома"
        )
    tracks_crud.delete(db_track)


@router.get('/{track_id}/playlists/my',  response_model=List[PlaylistInfoWithoutTracks])
def get_track_playlists(track_id: uuid_pkg.UUID = Path(..., description="ID трека"), Auth: Authenticate = Depends(Authenticate())):
    '''Получение ваших плейлистов, в которых есть трек'''
    tracks_crud = TracksCrud(db=Auth.db)
    track = tracks_crud.get_track(track_id=track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Трек не найден'
        )
    playlists = tracks_crud.get_my_track_playlists(
        track_id=track_id, user_id=Auth.current_user_id)
    for playlist in playlists:
        playlist.current_user_id = Auth.current_user_id
    return playlists


@router.get('/{track_id}/stats',  response_model=TrackStats)
def get_track_statistics(track_id: uuid_pkg.UUID= Path(..., description="ID трека"), Auth: Authenticate = Depends(Authenticate(is_admin=True, is_musician=True))):
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


@router.post('/{track_id}/listening',  status_code=status.HTTP_204_NO_CONTENT)
def start_listening_track(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
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


@router.put('/{track_id}/listening',  status_code=status.HTTP_204_NO_CONTENT)
def set_listened_track(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
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
    is_listened = tracks_crud.track_is_listened(
        last_listened=last_track_listen, time=datetime.now())
    if not is_listened:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Прослушивание трека начато слишком давно или еще не закончено")
    last_track_listen.listened = True
    tracks_crud.update(last_track_listen)


@router.get('/{track_id}/file', response_class=FileResponse)
def get_track_file(
    track_id: uuid_pkg.UUID = Path(..., description="ID трека"),
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
