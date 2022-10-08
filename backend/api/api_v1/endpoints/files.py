import os
from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from core.config import settings

router = APIRouter(prefix='/uploads')


@router.get('/images/{fileName}', response_class=FileResponse)
def get_image(fileName):
    file_name = secure_filename(fileName)
    file_path = os.path.join(settings.IMAGES_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type=f"image/{settings.IMAGES_EXTENTION[1:]}", filename=file_name)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
