import os
from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.responses import FileResponse
from backend.crud.crud_file import FileCruds
from backend.core.config import settings
from backend.db.db import get_db
from sqlalchemy.orm import Session
import uuid as uuid_pkg
from backend.helpers.images import image_id_to_path
router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])


@router.get('/images/{image_id}', response_class=FileResponse)
def get_image(
    image_id: uuid_pkg.UUID = Path(...,
                                   description="ID изображения"),
    db: Session = Depends(get_db)
):
    """Получение изображения по его id"""
    db_image = FileCruds(db).get_image_by_id(image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = image_id_to_path(image_id)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Файл не существует на сервере, но запись о нем есть")


@router.get('/other/{file_id}', response_class=FileResponse)
def get_file(file_id: uuid_pkg.UUID = Path(..., description="ID файла"), db: Session = Depends(get_db)):
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
