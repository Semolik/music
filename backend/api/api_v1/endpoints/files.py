import os
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from backend.crud.crud_music import music_crud
from backend.db.db import get_db
from backend.db.session import SessionLocal
from backend.crud.crud_file import file_cruds
from backend.core.config import settings

router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])
# folders = {
#     'image': settings.IMAGES_FOLDER,
#     'file': settings.OTHER_FILES_FOLDER,
#     'track': settings.TRACKS_FOLDER,
# }


@router.get('/images/{image_id}', response_class=FileResponse)
def get_image(image_id):
    db_image = file_cruds.get_image_by_id(image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.IMAGES_FOLDER,
                             image_id+settings.IMAGES_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/other/{file_id}', response_class=FileResponse)
def get_image(file_id):
    db_file = file_cruds.get_file_by_id(file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.OTHER_FILES_FOLDER,
                             file_id+db_file.extension)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/tracks/{track_id}', response_class=FileResponse)
def get_image(track_id):
    db_file = music_crud.get_track(track_id=track_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.TRACKS_FOLDER,
                             track_id+settings.SONGS_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")
# @router.get('/tracks/{fileName}', response_class=FileResponse)
# @router.get('/images/{fileName}', response_class=FileResponse)
# @router.get('/{fileName}', response_class=FileResponse)
# def get_file(fileName, db: SessionLocal = Depends(get_db)):
#     file_name = secure_filename(fileName)
#     db_file = file_cruds.get_file_by_name(file_name=file_name)
#     if not db_file:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     file_path = os.path.join(folders.get(db_file.type), file_name)
#     original_file_name: str = db_file.original_file_name
#     if os.path.exists(file_path):
#         return FileResponse(file_path, filename=original_file_name)
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
