from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.images import save_image
from backend.helpers.music import save_track, set_full_track_data, set_track_data
from backend.helpers.validate_role import validate_musician
from backend.models.music import Album
from backend.responses import NOT_FOUND_TRACK, NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.music import Liked,  Track, TrackAfterUpload, UploadTrackForm
router = APIRouter(prefix="/tracks", tags=['Треки'])


@router.post('/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload)
def upload_track(
    trackData: UploadTrackForm = Depends(UploadTrackForm),
    trackPicture: UploadFile = File(default=False),
    track: UploadFile = File(default=False),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Создание трека'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_album = AlbumsCruds(db).get_album(album_id=trackData.album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if not AlbumsCruds(db).album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    if db_album.uploaded:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Добавление треков в загруженный альбом запрещено")
    db_image = save_image(
        db=db,
        upload_file=trackPicture,
        user_id=current_user_id
    )
    db_track = save_track(
        db=db,
        upload_file=track,
        user_id=current_user_id,
        track=trackData,
        picture=db_image
    )
    return db_track.as_dict()


@router.post('/like', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Liked)
def like_track(
    track_id: str,
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
    return Liked(liked=liked)


@router.get('/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Track)
def get_track(
    id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение трека'''
    Authorize.jwt_optional()
    db_track = TracksCrud(db).get_track(track_id=id)
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
def like_track(
    page: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение лайкнутых треков'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    liked_tracks = TracksCrud(db).get_liked_tracks(
        user_id=current_user_id, page=page)
    return [set_full_track_data(db=db, track=track, user_id=current_user_id) for track in liked_tracks]
