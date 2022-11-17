import os
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from backend.db.db import get_db
from backend.db.session import SessionLocal
from backend.crud.crud_file import file_cruds
from backend.core.config import settings

router = APIRouter(prefix=settings.UPLOADS_ROUTE, tags=['Файлы'])
folders = {
    'image': settings.IMAGES_FOLDER,
    'file': settings.OTHER_FILES_FOLDER,
    'track': settings.TRACKS_FOLDER,
}


@router.get('/tracks/{fileName}', response_class=FileResponse)
@router.get('/images/{fileName}', response_class=FileResponse)
@router.get('/{fileName}', response_class=FileResponse)
def get_file(fileName, db: SessionLocal = Depends(get_db)):
    file_name = secure_filename(fileName)
    db_file = file_cruds.get_file_by_name(file_name=file_name)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    file_path = os.path.join(folders.get(db_file.type), file_name)
    original_file_name: str = db_file.original_file_name
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=original_file_name)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
