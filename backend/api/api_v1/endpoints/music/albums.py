from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import album_cruds
from backend.crud.crud_music import music_crud
from backend.crud.crud_user import user_cruds
from backend.helpers.albums import is_album_showed
from backend.helpers.images import save_image
from backend.helpers.music import set_album_info, set_album_tracks,  validate_genres
from backend.helpers.validate_role import validate_musician
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_ALBUM,  NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.music import AlbumAfterUpload, AlbumInfo, AlbumIsCLosed, AlbumWithTracks, CreateAlbumForm, UpdateAlbumForm

router = APIRouter(prefix="/albums", tags=['Альбомы'])


@router.post('/album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload)
def create_album(albumData: CreateAlbumForm = Depends(CreateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    genres = validate_genres(genres_ids=albumData.genres_ids)
    db_image = save_image(upload_file=albumPicture,
                          user_id=db_user.id)
    db_album = album_cruds.create_album(
        name=albumData.name, user_id=current_user_id, date=albumData.date, picture=db_image, genres=genres)
    album_obj = set_album_info(db_album=db_album)
    return album_obj


@router.put('/album/close-uploading', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumIsCLosed)
def close_album_uploading(album_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_album = music_crud.get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not album_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    db_album = album_cruds.close_uploading(album=db_album)
    return AlbumIsCLosed(closed_uploading=not db_album.uploaded)


@router.put('/album', responses={**UNAUTHORIZED_401, **NOT_ENOUGH_RIGHTS, **NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def create_album(albumData: UpdateAlbumForm = Depends(UpdateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_album = music_crud.get_album(album_id=albumData.id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not album_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    tracks_ids = albumData.tracks_ids
    if sorted(i.id for i in db_album.tracks) != sorted(tracks_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Переданые id треков не соответствуют трекам в альбоме")
    genres = validate_genres(genres_ids=albumData.genres_ids)
    db_image = save_image(upload_file=albumPicture,
                          user_id=current_user_id)
    db_album = album_cruds.update_album(album=db_album,
                                        name=albumData.name, date=albumData.date, genres=genres, image=db_image, tracks_ids=tracks_ids)
    album_obj = set_album_info(db_album=db_album)
    return set_album_tracks(db_album=db_album, db_album_obj=album_obj)


@router.get('/album', responses={**NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def get_album_by_id(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    db_album = music_crud.get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not is_album_showed(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    db_album_obj = set_album_info(db_album=db_album)
    return set_album_tracks(db_album=db_album, db_album_obj=db_album_obj, user_id=current_user_id)


@router.delete('/album', responses={**NOT_FOUND_ALBUM})
def get_album_by_id(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_album = music_crud.get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not album_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нет прав на удаление данного альбома")
    music_crud.delete_album(album=db_album)
    return {'detail': 'Альбом удален'}


@router.get('/get_my_albums', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_my_albums(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_musician = user_cruds.get_public_profile(user_id=current_user_id)
    return [
        set_album_info(db_album=db_album)
        for db_album in album_cruds.get_musician_albums(musician_id=db_musician.id)]
