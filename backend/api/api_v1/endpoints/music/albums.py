from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_musician import MusicianCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.helpers.auth_helper import validate_authorized_user
from backend.helpers.music import album_is_available, is_album_showed, save_track
from backend.helpers.images import save_image
from backend.helpers.music import set_album_info, set_album_tracks,  validate_genres
from backend.helpers.users import get_public_profile_as_dict, set_musician_info
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_ALBUM,  NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.music import AlbumAfterUpload, AlbumInfo, AlbumIsCLosed, AlbumWithTracks, CreateAlbum, TrackAfterUpload, UpdateAlbum, UploadTrackForm
from backend.helpers.images import save_image, set_picture
router = APIRouter(prefix="/albums", tags=['Альбомы'])


@router.post('', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload, status_code=status.HTTP_201_CREATED)
def create_album(
    albumData: CreateAlbum,
    albumPicture: UploadFile = File(..., description='Картинка альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Создание альбома'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.musician]
    )
    genres = validate_genres(db=db, genres_ids=albumData.genres_ids)
    db_image = save_image(db=db, upload_file=albumPicture,
                          user_id=db_user.id)
    db_album = AlbumsCruds(db).create_album(
        name=albumData.name, user_id=db_user.id, date=albumData.date, picture=db_image, genres=genres)
    album_obj = set_album_info(db_album=db_album)
    return album_obj


@router.put('/{album_id}/close-uploading', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumIsCLosed)
def close_album_uploading(
    album_id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Закрытие альбома для загрузки треков'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.musician]
    )
    db_album = AlbumsCruds(db).get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.musician_user_id != db_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав на закрытие альбома")
    if db_album.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Альбом уже доступен для прослушивания")

    db_album = AlbumsCruds(db).close_uploading(album=db_album)
    return AlbumIsCLosed(closed_uploading=not db_album.uploaded)


@router.put('/{album_id}', responses={**UNAUTHORIZED_401, **NOT_ENOUGH_RIGHTS, **NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def update_album(
    albumData: UpdateAlbum,
    album_id: int = Query(..., description='ID альбома'),
    albumPicture: UploadFile = File(
        default=False, description='Картинка альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Обновление альбома'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.musician]
    )
    db_album = AlbumsCruds(db).get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.musician_user_id != db_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    tracks_ids = albumData.tracks_ids
    if sorted(i.id for i in db_album.tracks) != sorted(tracks_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Переданые id треков не соответствуют трекам в альбоме")
    genres = validate_genres(db=db, genres_ids=albumData.genres_ids)
    db_image = save_image(db=db, upload_file=albumPicture,
                          user_id=db_user.id)
    db_album = AlbumsCruds(db).update_album(album=db_album,
                                            name=albumData.name, date=albumData.date, genres=genres, image=db_image, tracks_ids=tracks_ids)
    album_obj = set_album_info(db_album=db_album)
    return set_album_tracks(db=db, db_album=db_album, db_album_obj=album_obj)


@router.get('/my', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_my_albums(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение альбомов музыканта'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.musician]
    )
    db_musician = UserCruds(db).get_public_profile(user_id=db_user.id)
    albums = []
    for db_album in MusicianCrud(db).get_all_musician_albums(musician_id=db_musician.id):
        album_info = set_album_info(db_album=db_album)
        album_info['musician'] = get_public_profile_as_dict(
            db=db, public_profile_id=db_album.musician_id)
        albums.append(album_info)
    return albums


@router.put('/{album_id}/like', responses={**NOT_FOUND_ALBUM}, response_model=bool)
def album_like(
    album_id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Лайнуть альбом'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize=Authorize, db=db)
    db_album = album_is_available(
        album_id=album_id,
        db=db,
        user_id=db_user.id
    )
    return AlbumsCruds(db).toggle_album_like(album=db_album, user_id=db_user.id)


@router.get('/liked', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_liked_albums(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение лайкнутых альбомов'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize=Authorize, db=db)
    albums = []
    for db_album in AlbumsCruds(db).get_liked_albums(user_id=db_user.id):
        album_info = set_album_info(db_album=db_album)
        album_info['musician'] = get_public_profile_as_dict(
            db=db, public_profile_id=db_album.musician_id)
        albums.append(album_info)
    return albums


@router.get('/{album_id}', responses={**NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def get_album_by_id(
    album_id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Получение альбома по id'''
    Authorize.jwt_optional()
    album_cruds = AlbumsCruds(db)
    db_album = album_cruds.get_album(album_id=album_id)
    if not db_album or not db_album.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if not db_album.is_opened:
        db_user = validate_authorized_user(
            Authorize=Authorize, db=db,
            types=[settings.UserTypeEnum.musician]
        )
        if not album_cruds.album_belongs_to_user(album=db_album, user_id=db_user.id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Альбом не найден")
    db_album_obj = set_album_info(db_album=db_album)
    db_album_obj = set_musician_info(
        data=db_album_obj, public_profile_id=db_album.musician_id, db=db)
    return set_album_tracks(db=db, db_album=db_album, db_album_obj=db_album_obj, user_id=Authorize.get_jwt_subject())


@router.post('/{album_id}/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload, status_code=status.HTTP_201_CREATED)
def upload_track(
    album_id: int = Query(..., description='ID альбома'),
    trackData: UploadTrackForm = Depends(UploadTrackForm),
    trackPicture: UploadFile = File(..., description="Изображение трека"),
    track: UploadFile = File(..., description="Файл трека"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Создание трека'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.musician]
    )
    album_cruds = AlbumsCruds(db)
    db_album = album_cruds.get_album(album_id=album_id)
    if not db_album or (not db_album.uploaded and db_album.musician_user_id != db_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.musician_user_id != db_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете добавлять треки в чужой альбом")
    if db_album.uploaded:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Добавление треков в загруженный альбом запрещено")
    db_image = save_image(
        db=db,
        upload_file=trackPicture,
        user_id=db_user.id
    )
    db_track = save_track(
        album_id=album_id,
        db=db,
        upload_file=track,
        user_id=db_user.id,
        track=trackData,
        picture=db_image
    )
    track_obj = set_picture(db_track.as_dict(), db_image)
    return track_obj


@router.delete('/{album_id}', responses={**NOT_FOUND_ALBUM}, status_code=status.HTTP_204_NO_CONTENT)
def delete_album_by_id(
    album_id: int = Query(..., description='ID альбома'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Удаление альбома по id'''
    Authorize.jwt_required()
    album_cruds = AlbumsCruds(db)
    db_album = album_cruds.get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    db_user = validate_authorized_user(Authorize, db)

    if db_user.type != settings.UserTypeEnum.superuser and not album_cruds.album_belongs_to_user(album=db_album, user_id=db_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав на удаление данного альбома")
    album_cruds.delete_album(album=db_album)
