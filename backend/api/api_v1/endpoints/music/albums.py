from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_musician import MusicianCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.helpers.auth_helper import Authenticate
from backend.helpers.files import valid_content_length
from backend.helpers.music import album_is_available, save_track
from backend.helpers.images import save_image
from backend.helpers.music import set_album_info, set_album_tracks,  validate_genres
from backend.helpers.users import get_public_profile_as_dict, set_musician_info
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_ALBUM,  NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.base import LikesInfo
from backend.schemas.music import AlbumAfterUpload, AlbumInfo, AlbumIsCLosed, AlbumWithTracks, CreateAlbum, CreateAlbumJson, MusicianInfo, TrackAfterUpload, UpdateAlbum, UpdateAlbumJson, UploadTrackForm
from backend.helpers.images import save_image, set_picture
router = APIRouter(prefix="/albums", tags=['Альбомы'])


@router.post('', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload, status_code=status.HTTP_201_CREATED, dependencies=[Depends(valid_content_length(
    settings.MAX_IMAGE_FILE_SIZE_MB))])
def create_album(
    albumData: CreateAlbumJson,
    albumPicture: UploadFile = File(..., description='Картинка альбома'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Создание альбома'''
    genres = validate_genres(db=Auth.db, genres_ids=albumData.genres_ids)
    db_image = save_image(
        db=Auth.db,
        upload_file=albumPicture,
        user_id=Auth.current_user.id
    )
    db_album = AlbumsCruds(Auth.db).create_album(
        name=albumData.name,
        user_id=Auth.current_user.id,
        date=albumData.open_date,
        picture=db_image,
        genres=genres
    )
    album_obj = set_album_info(db_album=db_album)
    return album_obj


@router.put('/{album_id}/close-uploading', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, status_code=status.HTTP_204_NO_CONTENT)
def close_album_uploading(
    album_id: int = Query(..., description='ID альбома'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Закрытие альбома для загрузки треков'''

    db_album = AlbumsCruds(Auth.db).get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.musician_user_id != Auth.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав на закрытие альбома")
    if db_album.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Альбом уже доступен для прослушивания")

    AlbumsCruds(Auth.db).close_uploading(album=db_album)


@router.put('/{album_id}', responses={**UNAUTHORIZED_401, **NOT_ENOUGH_RIGHTS, **NOT_FOUND_ALBUM}, response_model=AlbumWithTracks, dependencies=[Depends(valid_content_length(
    settings.MAX_IMAGE_FILE_SIZE_MB))])
def update_album(
    albumData: UpdateAlbumJson,
    album_id: int = Query(..., description='ID альбома'),
    albumPicture: UploadFile = File(
        default=False, description='Картинка альбома'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Обновление альбома'''

    db_album = AlbumsCruds(Auth.db).get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.musician_user_id != Auth.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    tracks_ids = albumData.tracks_ids
    if sorted(i.id for i in db_album.tracks) != sorted(tracks_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Переданые id треков не соответствуют трекам в альбоме")
    genres = validate_genres(db=Auth.db, genres_ids=albumData.genres_ids)
    db_image = save_image(db=Auth.db, upload_file=albumPicture,
                          user_id=Auth.current_user.id)
    db_album = AlbumsCruds(Auth.db).update_album(album=db_album,
                                                 name=albumData.name, date=albumData.open_date, genres=genres, image=db_image, tracks_ids=tracks_ids)
    return db_album


@router.get('/my', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_my_albums(
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Получение альбомов музыканта'''

    db_musician = UserCruds(Auth.db).get_public_profile(
        user_id=Auth.current_user.id)
    albums = []
    albums_obj = []
    for album in albums:
        album_info = AlbumInfo.from_orm(album)
        album_info.musician = MusicianInfo.from_orm(db_musician)
        albums_obj.append(album_info)
    return albums


@router.put('/{album_id}/like', responses={**NOT_FOUND_ALBUM}, response_model=LikesInfo)
def album_like(
    album_id: int = Query(..., description='ID альбома'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Лайнуть альбом'''
    db_album = album_is_available(
        album_id=album_id,
        db=Auth.db,
        user_id=Auth.current_user_id
    )
    is_liked = AlbumsCruds(Auth.db).toggle_album_like(
        album=db_album, user_id=Auth.current_user_id)
    likes_count = AlbumsCruds(Auth.db).get_album_likes_count(album=db_album)
    return LikesInfo(liked=is_liked, likes_count=likes_count)


@router.get('/liked', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_liked_albums(
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение лайкнутых альбомов'''

    albums = []
    for db_album in AlbumsCruds(Auth.db).get_liked_albums(user_id=Auth.current_user_id):
        album_info = set_album_info(db_album=db_album)
        album_info['musician'] = get_public_profile_as_dict(
            db=Auth.db, public_profile_id=db_album.musician_id)
        albums.append(album_info)
    return albums


@router.get('/{album_id}', responses={**NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def get_album_by_id(
    album_id: int = Query(..., description='ID альбома'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение альбома по id'''
    album_cruds = AlbumsCruds(db=Auth.db)
    db_album = album_cruds.get_album(album_id=album_id)
    if not db_album or not db_album.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if not db_album.is_opened:
        if not Auth.current_user or album_cruds.album_belongs_to_user(album=db_album, user_id=Auth.current_user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Альбом не найден")
    db_album_obj = set_album_info(db_album=db_album)
    db_album_obj = set_musician_info(
        data=db_album_obj, public_profile_id=db_album.musician_id, db=Auth.db)
    return set_album_tracks(db=Auth.db, db_album=db_album, db_album_obj=db_album_obj, user_id=Auth.current_user_id)


@router.post('/{album_id}/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload, status_code=status.HTTP_201_CREATED, dependencies=[Depends(valid_content_length(
    settings.MAX_TRACK_FILE_SIZE_MB))])
def upload_track(
    album_id: int = Query(..., description='ID альбома'),
    trackData: UploadTrackForm = Depends(UploadTrackForm),
    trackPicture: UploadFile = File(..., description="Изображение трека"),
    track: UploadFile = File(..., description="Файл трека"),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Создание трека'''

    album_cruds = AlbumsCruds(Auth.db)
    db_album = album_cruds.get_album(album_id=album_id)
    if not db_album or (not db_album.uploaded and db_album.musician_user_id != Auth.current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.musician_user_id != Auth.current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете добавлять треки в чужой альбом")
    if db_album.uploaded:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Добавление треков в загруженный альбом запрещено")
    db_image = save_image(
        db=Auth.db,
        upload_file=trackPicture,
        user_id=Auth.current_user_id,
    )
    db_track = save_track(
        album_id=album_id,
        db=Auth.db,
        upload_file=track,
        user_id=Auth.current_user_id,
        track=trackData,
        picture=db_image
    )
    track_obj = set_picture(db_track.as_dict(), db_image)
    return track_obj


@router.delete('/{album_id}', responses={**NOT_FOUND_ALBUM}, status_code=status.HTTP_204_NO_CONTENT)
def delete_album_by_id(
    album_id: int = Query(..., description='ID альбома'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Удаление альбома по id'''

    album_cruds = AlbumsCruds(Auth.db)
    db_album = album_cruds.get_album(album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")

    if Auth.current_user.type != settings.UserTypeEnum.superuser and not album_cruds.album_belongs_to_user(album=db_album, user_id=Auth.current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав на удаление данного альбома")
    album_cruds.delete_album(album=db_album)
