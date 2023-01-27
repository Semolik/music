from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_genres import GenresCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.images import save_image, set_picture
from backend.helpers.validate_role import validate_admin
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_GENRE
from backend.schemas.error import GENRE_IS_NOT_UNIQUE
from backend.schemas.music import Genre, GenreBaseForm
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
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(db=db, user_id=current_user_id)
    if GenresCruds(db).get_genre_by_name(name=genreData.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Название жанра должно быть уникальным")
    db_image = save_image(db=db, upload_file=genrePicture,
                          user_id=current_user_id)
    db_genre = GenresCruds(db).create_genre(
        name=genreData.name, picture=db_image)
    return set_picture(db_genre.as_dict(), db_genre.picture)


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
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(db=db, user_id=current_user_id)
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    db_image = save_image(db=db, upload_file=genrePicture,
                          user_id=current_user_id)
    genre = GenresCruds(db).update_genre(
        name=genreData.name, picture=db_image, genre=genre)
    return set_picture(genre.as_dict(), genre.picture)


@router.get('',  response_model=List[Genre])
def get_genres(db: Session = Depends(get_db)):
    '''Получение всех жанров'''
    return [
        set_picture(genre.as_dict(), genre.picture)
        for genre in GenresCruds(db).get_genres()
    ]


@router.get('/{genre_id}', responses={**NOT_FOUND_GENRE}, response_model=Genre)
def get_genre(genre_id: int = Query(..., description="ID жанра"), db: Session = Depends(get_db)):
    '''Получение жанра по id'''
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    return set_picture(genre.as_dict(), genre.picture)


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
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(db=db, user_id=current_user_id)
    genre = GenresCruds(db).get_genre_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    genre = GenresCruds(db).detete_genre(genre_id=genre_id)
