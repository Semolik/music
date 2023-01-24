from datetime import datetime
import os
from fastapi import BackgroundTasks, APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import FileResponse
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_file import FileCruds
from backend.core.config import settings
from backend.db.db import get_db
from sqlalchemy.orm import Session
import uuid as uuid_pkg
from fastapi_jwt_auth import AuthJWT
router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])


@router.get('/images/{image_id}', response_class=FileResponse)
def get_image(
        image_id: uuid_pkg.UUID = Query(..., description="ID изображения"),
        db: Session = Depends(get_db)
):
    """Получение изображения по его id"""
    db_image = FileCruds(db).get_image_by_id(image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.IMAGES_FOLDER,
                             str(image_id)+settings.IMAGES_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/other/{file_id}', response_class=FileResponse)
def get_image(file_id: uuid_pkg.UUID = Query(..., description="ID файла"), db: Session = Depends(get_db)):
    """Получение файла по его id"""
    db_file = FileCruds(db).get_file_by_id(file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.OTHER_FILES_FOLDER,
                             str(file_id)+db_file.extension)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/tracks/{track_id}', response_class=FileResponse)
def get_image(background_tasks: BackgroundTasks, track_id: uuid_pkg.UUID = Query(..., description="ID трека"),
              db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """Получение трека по его id"""
    Authorize.jwt_optional()
    db_file = TracksCrud(db).get_track(track_id=track_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.TRACKS_FOLDER,
                             str(track_id)+settings.SONGS_EXTENTION)
    current_user_id = Authorize.get_jwt_subject()
    if os.path.exists(file_path):
        if current_user_id:
            background_tasks.add_task(
                TracksCrud(db).add_listened,
                track_id=track_id,
                user_id=current_user_id,
                time=datetime.now()
            )
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")
