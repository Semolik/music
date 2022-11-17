from datetime import datetime
from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_music import music_crud
from backend.crud.crud_user import user_cruds
from backend.helpers.images import set_picture
from backend.helpers.music import save_track, set_album_info, set_album_tracks, set_full_track_data, set_track_data, validate_genres
from backend.helpers.validate_role import validate_admin, validate_musician
from backend.models.music import Album
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_ALBUM, NOT_FOUND_GENRE,  NOT_FOUND_TRACK, NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.error import GENRE_IS_NOT_UNIQUE
from backend.schemas.track import AlbumAfterUpload, AlbumInfo, AlbumWithTracks, CreateAlbumForm, CreateGenre, CreateGenreForm, Genre, Track, TrackAfterUpload, UpdateAlbum, UpdateAlbumForm, UpdateGenreForm, UploadTrackForm
from backend.helpers.files import save_file


albums_router = APIRouter(tags=['Альбомы'])
tracks_router = APIRouter(tags=['Треки'])
genres_router = APIRouter(tags=['Жанры'])


@albums_router.post('/album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload)
def create_album(albumData: CreateAlbumForm = Depends(CreateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    genres = validate_genres(genres_ids=albumData.genres_ids)
    db_image = save_file(upload_file=albumPicture,
                         user_id=db_user.id, force_image=True)
    db_album = music_crud.create_album(
        name=albumData.name, user_id=current_user_id, date=albumData.date, picture=db_image, genres=genres)
    album_obj = set_album_info(db_album=db_album)
    return album_obj


@albums_router.put('/album', responses={**UNAUTHORIZED_401, **NOT_ENOUGH_RIGHTS, **NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def create_album(albumData: UpdateAlbumForm = Depends(UpdateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_album = music_crud.get_album(album_id=albumData.id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    tracks_ids = albumData.tracks_ids
    if sorted(i.id for i in db_album.tracks) != sorted(tracks_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Переданые id треков не соответствуют трекам в альбоме")
    current_user_id = Authorize.get_jwt_subject()
    if not user_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет прав изменять этот альбом")
    genres = validate_genres(genres_ids=albumData.genres_ids)
    db_image = save_file(upload_file=albumPicture,
                         user_id=current_user_id, force_image=True)
    db_album = music_crud.update_album(album=db_album,
                                       name=albumData.name, date=albumData.date, genres=genres, image=db_image, tracks_ids=tracks_ids)
    album_obj = set_album_info(db_album=db_album)
    return set_album_tracks(db_album=db_album, db_album_obj=album_obj)


@albums_router.get('/album', responses={**NOT_FOUND_ALBUM}, response_model=AlbumWithTracks)
def get_album_by_id(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    db_album = music_crud.get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    if db_album.open_date > datetime.now():
        current_user_id = Authorize.get_jwt_subject()
        if current_user_id is None or not user_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Альбом не найден")
    db_album_obj = set_album_info(db_album=db_album, validate_date=True)
    return set_album_tracks(db_album=db_album, db_album_obj=db_album_obj)


@albums_router.get('/get_my_albums', responses={**UNAUTHORIZED_401}, response_model=List[AlbumInfo])
def get_my_albums(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_musician = user_cruds.get_public_profile(user_id=current_user_id)
    return [
        set_album_info(db_album=db_album)
        for db_album in music_crud.get_musician_albums(musician_id=db_musician.id)]


@albums_router.delete('/album', responses={**NOT_FOUND_ALBUM})
def get_album_by_id(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_album = music_crud.get_album(album_id=id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    current_user_id = Authorize.get_jwt_subject()
    if not user_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нет прав на удаление данного альбома")
    music_crud.delete_album(album=db_album)
    return {'detail': 'Альбом удален'}


@tracks_router.post('/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload)
def upload_track(trackData: UploadTrackForm = Depends(UploadTrackForm), trackPicture: UploadFile = File(default=False), track: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=trackPicture,
                         user_id=db_user.id, force_image=True)
    db_track = save_track(
        upload_file=track, user_id=current_user_id, track=trackData, picture=db_image)
    return db_track.as_dict()


@tracks_router.get('/track', responses={**UNAUTHORIZED_401, **NOT_FOUND_TRACK}, response_model=Track)
def get_track(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    db_track = music_crud.get_track(track_id=id)
    if not db_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    db_album: Album = db_track.album
    if db_album.open_date > datetime.now():
        current_user_id = Authorize.get_jwt_subject()
        if current_user_id is None or not user_cruds.album_belongs_to_user(album=db_album, user_id=current_user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Трек не найден")
    return set_full_track_data(db_track)


@genres_router.get('/genres',  response_model=List[Genre])
def get_genres():
    return [set_picture(genre.as_dict(), genre.picture) for genre in music_crud.get_genres()]


@genres_router.get('/genre', responses={**NOT_FOUND_GENRE}, response_model=Genre)
def get_genre(id: int):
    genre = music_crud.get_genre_by_id(id=id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    return set_picture(genre.as_dict(), genre.picture)


@genres_router.post('/genre', responses={**NOT_ENOUGH_RIGHTS, status.HTTP_409_CONFLICT: {"model": GENRE_IS_NOT_UNIQUE}}, response_model=Genre)
def create_genre(genreData: CreateGenreForm = Depends(CreateGenreForm), genrePicture: UploadFile = File(...), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(user_id=current_user_id)
    if music_crud.get_genre_by_name(name=genreData.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Название жанра должно быть уникальным")
    db_image = save_file(upload_file=genrePicture,
                         user_id=current_user_id, force_image=True)
    db_genre = music_crud.create_genre(name=genreData.name, picture=db_image)
    return set_picture(db_genre.as_dict(), db_genre.picture)


@genres_router.put('/genre', responses={**NOT_ENOUGH_RIGHTS, **NOT_FOUND_GENRE}, response_model=Genre)
def update_genre(genreData: UpdateGenreForm = Depends(UpdateGenreForm), genrePicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(user_id=current_user_id)
    genre = music_crud.get_genre_by_id(id=genreData.id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    db_image = save_file(upload_file=genrePicture,
                         user_id=current_user_id, force_image=True)
    genre = music_crud.update_genre(
        name=genreData.name, picture=db_image, genre=genre)
    return set_picture(genre.as_dict(), genre.picture)


@genres_router.delete('/genre', responses={**NOT_ENOUGH_RIGHTS, **NOT_FOUND_GENRE})
def delete_genre(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(user_id=current_user_id)
    genre = music_crud.get_genre_by_id(id=id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    genre = music_crud.detete_genre(genre_id=id)
    return {'detail': 'Жанр удален'}


router = APIRouter()
router.include_router(albums_router)
router.include_router(tracks_router)
router.include_router(genres_router)
