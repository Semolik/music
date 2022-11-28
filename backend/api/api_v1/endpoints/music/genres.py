from typing import List
from fastapi import Depends, APIRouter,  UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_music import music_crud
from backend.helpers.images import save_image, set_picture
from backend.helpers.validate_role import validate_admin
from backend.responses import NOT_ENOUGH_RIGHTS, NOT_FOUND_GENRE
from backend.schemas.error import GENRE_IS_NOT_UNIQUE
from backend.schemas.music import CreateGenreForm, Genre, UpdateGenreForm
from backend.helpers.files import save_file
router = APIRouter(prefix="/genres", tags=['Жанры'])


@router.post('/genre', responses={**NOT_ENOUGH_RIGHTS, status.HTTP_409_CONFLICT: {"model": GENRE_IS_NOT_UNIQUE}}, response_model=Genre)
def create_genre(genreData: CreateGenreForm = Depends(CreateGenreForm), genrePicture: UploadFile = File(...), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(user_id=current_user_id)
    if music_crud.get_genre_by_name(name=genreData.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Название жанра должно быть уникальным")
    db_image = save_image(upload_file=genrePicture,
                          user_id=current_user_id)
    db_genre = music_crud.create_genre(name=genreData.name, picture=db_image)
    return set_picture(db_genre.as_dict(), db_genre.picture)


@router.put('/genre', responses={**NOT_ENOUGH_RIGHTS, **NOT_FOUND_GENRE}, response_model=Genre)
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


@router.get('/all',  response_model=List[Genre])
def get_genres():
    return [set_picture(genre.as_dict(), genre.picture) for genre in music_crud.get_genres()]


@router.get('/genre', responses={**NOT_FOUND_GENRE}, response_model=Genre)
def get_genre(id: int):
    genre = music_crud.get_genre_by_id(id=id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Жанр не найден")
    return set_picture(genre.as_dict(), genre.picture)


@router.delete('/genre', responses={**NOT_ENOUGH_RIGHTS, **NOT_FOUND_GENRE})
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
