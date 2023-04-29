from typing import List
from fastapi import Depends, APIRouter, Path,  UploadFile, File, status, HTTPException
from backend.crud.crud_genres import GenresCruds
from backend.helpers.auth_helper import Authenticate
from backend.helpers.files import valid_content_length
from backend.helpers.images import save_image
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_GENRE
from backend.schemas.error import GENRE_IS_NOT_UNIQUE
from backend.schemas.music import Genre, GenreBaseForm, GenreFullInfo
from backend.core.config import settings
from backend.schemas.statistics import GenreStats

router = APIRouter(prefix="/genres", tags=['Жанры'])


@router.post('', responses={**NOT_ENOUGH_RIGHTS, status.HTTP_409_CONFLICT: {"model": GENRE_IS_NOT_UNIQUE}}, response_model=GenreStats, dependencies=[Depends(valid_content_length(
    settings.MAX_IMAGE_FILE_SIZE_MB))])
def create_genre(
    genreData: GenreBaseForm = Depends(GenreBaseForm),
    genrePicture: UploadFile = File(..., description='Картинка жанра'),
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Создание жанра'''

    if GenresCruds(Auth.db).get_genre_by_name(name=genreData.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Название жанра должно быть уникальным")
    db_image = save_image(db=Auth.db, upload_file=genrePicture,
                          user_id=Auth.current_user_id, resize_image_options=(1000, 1000))
    db_genre = GenresCruds(Auth.db).create_genre(
        name=genreData.name, picture=db_image)
    return db_genre


@router.get('/random',  response_model=List[Genre])
def get_random_genres(Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Получение случайных жанров'''
    genres = GenresCruds(Auth.db).get_random_genres()
    if Auth.current_user_id:
        for genre in genres:
            genre.current_user_id = Auth.current_user_id
    return genres


@router.put('/{genre_id}/like', response_model=bool)
def like_genre(
    genre_id: int = Path(..., description='ID жанра', ge=1),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Лайк жанра'''

    genre = GenresCruds(Auth.db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    return GenresCruds(Auth.db).toggle_like_genre(user_id=Auth.current_user_id, genre_id=genre.id)


@router.put(
    '/{genre_id}',
    responses={
        **NOT_ENOUGH_RIGHTS,
        **NOT_FOUND_GENRE
    },
    response_model=GenreStats,
    dependencies=[Depends(valid_content_length(
        settings.MAX_IMAGE_FILE_SIZE_MB))]
)
def update_genre(
    genre_id: int = Path(..., description='ID жанра', ge=1),
    genreData: GenreBaseForm = Depends(GenreBaseForm),
    genrePicture: UploadFile = File(None, description='Картинка жанра'),
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Обновление жанра'''

    genre = GenresCruds(Auth.db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    db_image = save_image(db=Auth.db, upload_file=genrePicture,
                          user_id=Auth.current_user_id)
    genre = GenresCruds(Auth.db).update_genre(
        name=genreData.name, picture=db_image, genre=genre)
    genre.current_user_id = Auth.current_user_id
    return genre


@router.get(
    '/{genre_id}',
    responses={**NOT_FOUND_GENRE},
    response_model=GenreFullInfo)
def get_genre(genre_id: int = Path(..., description="ID жанра", ge=1), Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Получение информации о жанре'''
    genre = GenresCruds(Auth.db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    genre_obj = GenreFullInfo.from_orm(genre)
    genre_obj.liked = bool(
        GenresCruds(Auth.db).get_liked_genre_model(
            user_id=Auth.current_user_id, genre_id=genre.id)
    ) if Auth.current_user_id else False
    popular_albums = GenresCruds(Auth.db).get_popular_albums_by_genre_id(
        page=1,
        genre_id=genre_id
    )
    new_albums = GenresCruds(Auth.db).get_new_albums_by_genre_id(
        page=1,
        genre_id=genre_id
    )
    popular_tracks = GenresCruds(Auth.db).get_popular_tracks_by_genre_id(
        page=1,
        genre_id=genre_id
    )
    popular_musicians = GenresCruds(Auth.db).get_popular_musicians_by_genre_id(
        page=1,
        genre_id=genre_id
    )
    for album in popular_albums:
        album.current_user_id = Auth.current_user_id

    for album in new_albums:
        album.current_user_id = Auth.current_user_id

    for track in popular_tracks:
        track.current_user_id = Auth.current_user_id

    for musician in popular_musicians:
        musician.current_user_id = Auth.current_user_id

    genre_obj.popular_albums = popular_albums
    genre_obj.new_albums = new_albums
    genre_obj.popular_tracks = popular_tracks
    genre_obj.popular_musicians = popular_musicians
    return genre_obj


@router.get(
    '/{genre_id}/stats',
    responses={
        **NOT_ENOUGH_RIGHTS,
        **NOT_FOUND_GENRE
    },
    response_model=GenreStats)
def get_genre_info(genre_id: int = Path(..., ge=1), Auth: Authenticate = Depends(Authenticate(is_admin=True))):
    '''Получение статистики по жанру'''
    genre = GenresCruds(db=Auth.db).get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Жанр не найден'
        )
    genre.current_user_id = Auth.current_user_id
    return genre


@router.delete(
    '/{genre_id}',
    responses={
        **NOT_ENOUGH_RIGHTS,
        **NOT_FOUND_GENRE
    },
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_genre(genre_id: int = Path(..., description="ID жанра", ge=1), Auth: Authenticate = Depends(Authenticate(is_admin=True))):
    '''Удаление жанра'''

    genre = GenresCruds(Auth.db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    GenresCruds(Auth.db).detete_genre(genre=genre)


@router.get('',  response_model=List[Genre])
def get_genres(
    page: int = 1,
    filter: settings.FilterGenreEnum = settings.FilterGenreEnum.all,
    Auth: Authenticate = Depends(Authenticate(required=False))
):
    '''Получение  жанров отсортированных по популярности'''
    if filter != settings.FilterGenreEnum.all and not Auth.current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Для фильтрации жанров необходимо авторизоваться")
    genres = GenresCruds(Auth.db).get_popular_genres(
        page=page, page_size=settings.SEARCH_GENRE_LIMIT, filter=filter, current_user_id=Auth.current_user_id)
    for genre in genres:
        genre.current_user_id = Auth.current_user_id
    return genres
