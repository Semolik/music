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


def set_picture(user_data: dict, picture: File):
    if picture:
        user_data['picture'] = ''.join(
            [settings.SERVER_LINK, settings.API_V1_STR,  settings.UPLOADS_ROUTE, '/images/', picture.file_name])
    return user_data
