import io
from typing import List
from PIL import Image as pillow
import logging
import shutil
from fastapi.encoders import jsonable_encoder
from backend.helpers.images import save_image
from backend.models.files import File
from fastapi import UploadFile
from backend.schemas.file import File as FileSchema
from backend.core.config import settings
from backend.crud.crud_file import FileCruds
from sqlalchemy.orm import Session
from pathlib import Path
import requests
import shutil
logger = logging.getLogger(__name__)
supported_image_extensions = {
    ex for ex, f in pillow.registered_extensions().items() if f in pillow.OPEN}


def init_folders_structure():
    pathes = [Path(path) for path in [settings.IMAGES_FOLDER,
                                      settings.OTHER_FILES_FOLDER,
                                      settings.TRACKS_FOLDER]]
    flag = False
    for path in pathes:
        if not path.exists():
            if not flag:
                logger.info("Создание структуры папок")
            flag = True
            path.mkdir(parents=True, exist_ok=True)
    if flag:
        logger.info("Структура папок создана")


def save_file(db: Session, upload_file: UploadFile, user_id: int) -> File | None:
    if not upload_file or not upload_file.filename:
        return
    original_file_name = upload_file.filename
    suffix = Path(original_file_name).suffix
    file_model = FileCruds(db).create_file(
        user_id=user_id, original_file_name=original_file_name, extension=suffix)
    fileName = str(file_model.id) + suffix
    with open('/'.join([settings.OTHER_FILES_FOLDER, fileName]), "wb+") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    upload_file.file.close()
    return file_model


def set_files_data(files: List[File]):
    return [set_file_data(file) for file in files]


def set_file_data(file: File) -> FileSchema:
    file_obj = jsonable_encoder(file)
    str_file_id = str(file.id)
    chapters = [
        ''.join(
            [
                settings.SERVER_LINK,
                settings.API_V1_STR,
                settings.UPLOADS_ROUTE,
                settings.OTHER_FILES_ROUTE,
                str_file_id
            ]
        )
    ]
    file_obj['url'] = '/'.join(chapters)
    file_obj['file_name'] = str_file_id + file.extension
    return file_obj


def save_image_in_db_by_url(db: Session, url: str, user_id: int) -> File | None:
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        buf = io.BytesIO()
        shutil.copyfileobj(r.raw, buf)
        buf.name = url.split('/')[-1]
        buf.seek(0)
        return save_image(db=db, upload_file=None, user_id=user_id, bytes_io_file=buf, resize_image_options=(1000, 1000), detail_error_message="не удалось скачать обложку ролика")
