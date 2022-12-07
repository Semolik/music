from backend.models.files import Image
from backend.core.config import settings
import io
from PIL import Image as pillow
import logging
import shutil
from fastapi import UploadFile, HTTPException
from backend.crud.crud_file import FileCruds
from pathlib import Path
from sqlalchemy.orm import Session
logger = logging.getLogger(__name__)
supported_image_extensions = {
    ex for ex, f in pillow.registered_extensions().items() if f in pillow.OPEN}


def set_picture(data: dict, picture: Image):
    if picture:
        data['picture'] = ''.join(
            [settings.SERVER_LINK, settings.API_V1_STR,  settings.UPLOADS_ROUTE, '/images/', str(picture.id)])
    return data


def save_image(db: Session, upload_file: UploadFile, user_id: int, resize_image_options=(400, 400), bytes_io_file: io.BytesIO = None, detail_error_message="поврежденный файл"):
    if (not upload_file or not upload_file.filename) if not bytes_io_file else False:
        return
    if bytes_io_file:
        originalFileName = bytes_io_file.name
    else:
        originalFileName = upload_file.filename
    originalFilePath = Path(originalFileName)
    suffix = originalFilePath.suffix
    if suffix.lower() not in supported_image_extensions:
        raise HTTPException(
            status_code=500, detail="Расширение изображения не поддерживается")
    if bytes_io_file:
        buf = bytes_io_file
    else:
        buf = io.BytesIO()
        shutil.copyfileobj(upload_file.file, buf)
        buf.seek(0)
    try:
        image = pillow.open(buf)
        image.thumbnail(resize_image_options)
        image_model = FileCruds(db).create_image(
            width=image.width, height=image.height, user_id=user_id)
        image.save('/'.join([settings.IMAGES_FOLDER,
                            str(image_model.id)+settings.IMAGES_EXTENTION]))
        return image_model
    except:
        raise HTTPException(status_code=500, detail=detail_error_message)
