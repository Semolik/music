from datetime import datetime
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import album_cruds
from backend.crud.crud_music import music_crud
from backend.crud.crud_user import user_cruds
from backend.helpers.images import save_image
from backend.helpers.music import save_track, set_full_track_data
from backend.helpers.validate_role import validate_musician
from backend.models.music import Album
from backend.responses import NOT_FOUND_TRACK, NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.music import Liked,  Track, TrackAfterUpload, UploadTrackForm
router = APIRouter(prefix="/tracks", tags=['Треки'])


@router.post('/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload)
def upload_track(trackData: UploadTrackForm = Depends(UploadTrackForm), trackPicture: UploadFile = File(default=False), track: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_album = music_crud.get_album(album_id=trackData.album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if not album_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    if db_album.uploaded:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Добавление треков в загруженный альбом запрещено")
    db_image = save_image(upload_file=trackPicture,
                          user_id=current_user_id)
    db_track = save_track(
        upload_file=track, user_id=current_user_id, track=trackData, picture=db_image)
    return db_track.as_dict()


@router.post('/like', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Liked)
def like_track(track_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_track = music_crud.get_track(track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    current_user_id = Authorize.get_jwt_subject()
    liked = music_crud.toggle_like_track(
        track_id=db_track.id, user_id=current_user_id)
    return Liked(liked=liked)


@router.get('/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Track)
def get_track(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    db_track = music_crud.get_track(track_id=id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    db_album: Album = db_track.album
    current_user_id = Authorize.get_jwt_subject()
    if db_album.open_date > datetime.now():
        if current_user_id is None or not user_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Трек не найден")
    return set_full_track_data(db_track, user_id=current_user_id)