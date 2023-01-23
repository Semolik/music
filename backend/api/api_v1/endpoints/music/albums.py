from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_musician import MusicianCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.helpers.music import is_album_showed
from backend.helpers.images import save_image
from backend.helpers.music import set_album_info, set_album_tracks,  validate_genres
from backend.helpers.users import get_public_profile_as_dict, set_musician_info
from backend.helpers.validate_role import validate_musician
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_ALBUM,  NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.music import AlbumAfterUpload, AlbumInfo, AlbumIsCLosed, AlbumWithTracks, CreateAlbumForm, UpdateAlbumForm

router = APIRouter(prefix="/albums", tags=['Альбомы'])


@router.post('/album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload)
def create_album(
    albumData: CreateAlbumForm = Depends(CreateAlbumForm),
    albumPicture: UploadFile = File(
        default=False, description='Картинка альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Создание альбома'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(db=db, user_id=current_user_id)
    genres = validate_genres(db=db, genres_ids=albumData.genres_ids)
    db_image = save_image(db=db, upload_file=albumPicture,
                          user_id=db_user.id)
    db_album = AlbumsCruds(db).create_album(
        name=albumData.name, user_id=current_user_id, date=albumData.date, picture=db_image, genres=genres)
    album_obj = set_album_info(db_album=db_album)
    return album_obj


@router.put('/album/close-uploading', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumIsCLosed)
def close_album_uploading(
    album_id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Закрытие альбома для загрузки треков'''
    Authorize.jwt_required()
    db_album = AlbumsCruds(db).get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not AlbumsCruds(db).album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    db_album = AlbumsCruds(db).close_uploading(album=db_album)
    return AlbumIsCLosed(closed_uploading=not db_album.uploaded)


@router.put('/album', responses={**UNAUTHORIZED_401, **NOT_ENOUGH_RIGHTS, **NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def create_album(
    albumData: UpdateAlbumForm = Depends(UpdateAlbumForm),
    albumPicture: UploadFile = File(
        default=False, description='Картинка альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Обновление альбома'''
    Authorize.jwt_required()
    db_album = AlbumsCruds(db).get_album(album_id=albumData.id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not AlbumsCruds(db).album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    tracks_ids = albumData.tracks_ids
    if sorted(i.id for i in db_album.tracks) != sorted(tracks_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Переданые id треков не соответствуют трекам в альбоме")
    genres = validate_genres(db=db, genres_ids=albumData.genres_ids)
    db_image = save_image(db=db, upload_file=albumPicture,
                          user_id=current_user_id)
    db_album = AlbumsCruds(db).update_album(album=db_album,
                                            name=albumData.name, date=albumData.date, genres=genres, image=db_image, tracks_ids=tracks_ids)
    album_obj = set_album_info(db=db, db_album=db_album)
    return set_album_tracks(db=db, db_album=db_album, db_album_obj=album_obj)


@router.get('/album', responses={**NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def get_album_by_id(
    id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение альбома по id'''
    Authorize.jwt_optional()
    db_album = AlbumsCruds(db).get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not is_album_showed(db=db, album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    db_album_obj = set_album_info(db_album=db_album)
    db_album_obj = set_musician_info(
        data=db_album_obj, public_profile_id=db_album.musician_id, db=db)
    return set_album_tracks(db=db, db_album=db_album, db_album_obj=db_album_obj, user_id=current_user_id)


@router.delete('/album', responses={**NOT_FOUND_ALBUM})
def get_album_by_id(
    id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Удаление альбома по id'''
    Authorize.jwt_required()
    db_album = AlbumsCruds(db).get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not AlbumsCruds(db).album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нет прав на удаление данного альбома")
    AlbumsCruds(db).delete_album(album=db_album)
    return {'detail': 'Альбом удален'}


@router.get('/get_my_albums', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_my_albums(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение альбомов музыканта'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(db=db, user_id=current_user_id)
    db_musician = UserCruds(db).get_public_profile(user_id=current_user_id)
    albums = []
    for db_album in MusicianCrud(db).get_musician_albums(musician_id=db_musician.id):

        album_info = set_album_info(db_album=db_album)
        album_info['musician'] = get_public_profile_as_dict(
            db=db, public_profile_id=db_album.musician_id)
        albums.append(album_info)
    return albums
