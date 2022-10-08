import os
from sqlalchemy.orm import Session
from db.base import CRUDBase
from db.session import SessionLocal
from schemas.user import UserAuth, UserModifiable, UserRegister
from models.user import File, User
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from pathlib import Path
from core.config import settings


class FileCruds:
    def __init__(self, db: Session) -> None:
        self.db = db

    def delete_file(self, file: File) -> None:
        if Path(file.file_name).suffix == settings.IMAGES_EXTENTION:
            path = '/'.join([settings.IMAGES_FOLDER,file.file_name])
            if Path(path).exists():
                os.remove(path)
            self.db.delete(file)
            self.db.commit()
        else:
            raise Exception('Удаление не картинки еще не написано')
