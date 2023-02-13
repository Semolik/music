from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_genres import GenresCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth_helper import validate_authorized_user
from backend.helpers.images import save_image, set_picture
from backend.helpers.music import validate_genres
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_GENRE
from backend.schemas.error import GENRE_IS_NOT_UNIQUE
from backend.schemas.music import Genre, GenreBaseForm
from backend.core.config import settings
router = APIRouter(prefix="/genres", tags=['Жанры'])


@router.post('', responses={**NOT_ENOUGH_RIGHTS, status.HTTP_409_CONFLICT: {"model": GENRE_IS_NOT_UNIQUE}}, response_model=Genre)
def create_genre(
    genreData: GenreBaseForm = Depends(GenreBaseForm),
    genrePicture: UploadFile = File(..., description='Картинка жанра'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Создание жанра'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.superuser]
    )
    if GenresCruds(db).get_genre_by_name(name=genreData.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Название жанра должно быть уникальным")
    db_image = save_image(db=db, upload_file=genrePicture,
                          user_id=db_user.id)
    db_genre = GenresCruds(db).create_genre(
        name=genreData.name, picture=db_image)
    return db_genre


@router.put('/{genre_id}/like', response_model=bool)
def like_genre(
    genre_id: int = Query(..., description='ID жанра'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Лайк жанра'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
    )
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    return GenresCruds(db).toggle_like_genre(user_id=db_user.id, genre_id=genre.id)


@router.put(
    '/{genre_id}',
    responses={
        **NOT_ENOUGH_RIGHTS,
        **NOT_FOUND_GENRE
    },
    response_model=Genre
)
def update_genre(
    genre_id: int = Query(..., description='ID жанра'),
    genreData: GenreBaseForm = Depends(GenreBaseForm),
    genrePicture: UploadFile = File(None, description='Картинка жанра'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Обновление жанра'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.superuser]
    )
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    db_image = save_image(db=db, upload_file=genrePicture,
                          user_id=db_user.id) if genrePicture else None
    genre = GenresCruds(db).update_genre(
        name=genreData.name, picture=db_image, genre=genre)
    return genre


@router.get('/{genre_id}', responses={**NOT_FOUND_GENRE}, response_model=Genre)
def get_genre(genre_id: int = Query(..., description="ID жанра"), db: Session = Depends(get_db)):
    '''Получение жанра по id'''
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    return genre


@router.delete(
    '/{genre_id}',
    responses={
        **NOT_ENOUGH_RIGHTS,
        **NOT_FOUND_GENRE
    },
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_genre(genre_id: int = Query(..., description="ID жанра"), Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Удаление жанра'''
    Authorize.jwt_required()
    validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.superuser]
    )
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    GenresCruds(db).detete_genre(genre=genre)


@router.get('',  response_model=List[Genre])
def get_genres(db: Session = Depends(get_db)):
    '''Получение всех жанров'''
    return GenresCruds(db).get_genres()
