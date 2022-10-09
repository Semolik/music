import io
import shutil
from fastapi import UploadFile, HTTPException, Depends
from PIL import Image
import uuid
# from schemas.file import File
from db.base import CRUDBase
from models.user import File, User
# import models.user as user_models
from core.config import settings
from db.session import Session
from db.db import get_db


def save_image(upload_file: UploadFile, user: User, db: Session = Depends(get_db)):
    if not upload_file.filename:
        return
    buf = io.BytesIO()
    shutil.copyfileobj(upload_file.file, buf)
    buf.seek(0)
    try:
        image = Image.open(buf)
        image.thumbnail((600, 600))
        fileName = str(uuid.uuid4()) + settings.IMAGES_EXTENTION
        image.save('/'.join([settings.IMAGES_FOLDER, fileName]))
    except:
        raise HTTPException(status_code=500, detail="поврежденный файл")
    # file_obj = File(file_name=fileName, user_id=user.id)
    # return CRUDBase(user_models.File).create(obj_in=file_obj)
    return File(file_name=fileName, user_id=user.id)


def set_picture(user_data: dict, picture: File):
    if picture:
        user_data['picture'] = ''.join(
            [settings.SERVER_LINK, settings.API_V1_STR,  settings.UPLOADS_ROUTE, '/images/', picture.file_name])
    return user_data
