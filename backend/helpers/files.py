import io
from PIL import Image
import os
import logging
import shutil
import uuid
from models.user import File
from fastapi import UploadFile, HTTPException
from core.config import settings
from pathlib import Path
logger = logging.getLogger(__name__)
supported_image_extensions = {
    ex for ex, f in Image.registered_extensions().items() if f in Image.OPEN}


def init_folders_structure():
    pathes = [Path(path) for path in [settings.IMAGES_FOLDER,
                                      settings.OTHER_FILES_FOLDER]]
    flag = False
    for path in pathes:
        if not path.exists():
            if not flag:
                logger.info("Создание структуры папок")
            flag = True
            path.mkdir(parents=True, exist_ok=True)
    if flag:
        logger.info("Структура папок создана")


def save_file(upload_file: UploadFile, user_id: int) -> File:
    if not upload_file.filename:
        return
    originalFileName = upload_file.filename
    originalFilePath = Path(originalFileName)
    suffix = originalFilePath.suffix
    uuid_filename = str(uuid.uuid4())
    if suffix in supported_image_extensions:
        buf = io.BytesIO()
        shutil.copyfileobj(upload_file.file, buf)
        buf.seek(0)
        try:
            image = Image.open(buf)
            image.thumbnail((600, 600))
            fileName = uuid_filename + settings.IMAGES_EXTENTION
            image.save('/'.join([settings.IMAGES_FOLDER, fileName]))
        except:
            raise HTTPException(status_code=500, detail="поврежденный файл")
        return File(file_name=fileName, original_file_name=originalFileName, user_id=user_id, type='image')
    else:
        fileName = uuid_filename + suffix
        with open('/'.join([settings.OTHER_FILES_FOLDER, fileName]), "wb+") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        upload_file.file.close()
        return File(file_name=fileName, original_file_name=originalFileName, user_id=user_id)
