import os
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_file import FileCruds
from backend.core.config import settings
from backend.db.db import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])


@router.get('/images/{image_id}', response_class=FileResponse)
def get_image(image_id, db: Session = Depends(get_db)):
    db_image = FileCruds(db).get_image_by_id(image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.IMAGES_FOLDER,
                             image_id+settings.IMAGES_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/other/{file_id}', response_class=FileResponse)
def get_image(file_id: int, db: Session = Depends(get_db)):
    db_file = FileCruds(db).get_file_by_id(file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.OTHER_FILES_FOLDER,
                             file_id+db_file.extension)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/tracks/{track_id}', response_class=FileResponse)
def get_image(track_id, db: Session = Depends(get_db)):
    db_file = TracksCrud(db).get_track(track_id=track_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.TRACKS_FOLDER,
                             track_id+settings.SONGS_EXTENTION)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")
