from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_music import music_crud
from backend.crud.crud_user import user_cruds
from backend.helpers.music import save_track, set_album_info
from backend.helpers.validate_role import validate_musician
from backend.responses import NOT_FOUND_ALBUM, NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.track import AlbumAfterUpload, AlbumInfo, CreateAlbumForm, TrackAfterUpload, UploadTrackForm
from backend.helpers.files import save_file

router = APIRouter(tags=['Музыка'])


@router.post('/create_album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload)
def create_album(albumData: CreateAlbumForm = Depends(CreateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=albumPicture,
                         user_id=db_user.id, force_image=True)
    db_album = music_crud.create_album(
        name=albumData.name, user_id=current_user_id, date=albumData.date, picture=db_image)
    return set_album_info(db_album=db_album)


@router.post('/upload_song', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload)
def upload_song(trackData: UploadTrackForm = Depends(UploadTrackForm), trackPicture: UploadFile = File(default=False), track: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=trackPicture,
                         user_id=db_user.id, force_image=True)
    db_track = save_track(
        upload_file=track, user_id=current_user_id, track=trackData, picture=db_image)
    return db_track.as_dict()


@router.get('/get_my_albums', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_my_albums(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_musician = user_cruds.get_public_profile(user_id=current_user_id)
    return [
        set_album_info(db_album=db_album)
        for db_album in music_crud.get_musician_albums(musician_id=db_musician.id)]


@router.get('/get_album', responses={**NOT_FOUND_ALBUM}, response_model=AlbumInfo)
def get_album_by_id(id: int):
    db_album = music_crud.get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    return set_album_info(db_album=db_album)
