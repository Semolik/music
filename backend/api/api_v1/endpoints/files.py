import os
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from backend.db.db import get_db
from backend.db.session import SessionLocal
from backend.crud.crud_file import FileCruds
from backend.core.config import settings

router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])


@router.get('/images/{fileName}', response_class=FileResponse)
@router.get('/{fileName}', response_class=FileResponse)
def get_file(fileName, db: SessionLocal = Depends(get_db)):
    file_name = secure_filename(fileName)
    db_file = FileCruds(db).get_file_by_name(file_name=file_name)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(settings.IMAGES_FOLDER if db_file.type ==
                             'image' else settings.OTHER_FILES_FOLDER, file_name)
    original_file_name: str = db_file.original_file_name
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=original_file_name)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
