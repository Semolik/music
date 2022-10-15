import os
from sqlalchemy.orm import Session
from db.db import get_db
from models.user import File
from pathlib import Path
from core.config import settings


class FileCruds:
    def __init__(self, db: Session = get_db()) -> None:
        self.db = db

    def delete_file(self, file: File) -> None:
        if file.type == 'image':
            path = '/'.join([settings.IMAGES_FOLDER, file.file_name])
            if Path(path).exists():
                os.remove(path)
            self.db.delete(file)
            self.db.commit()
        else:
            raise Exception('Удаление не картинки еще не написано')

    def get_file_by_name(self, file_name: str):
        return self.db.query(File).filter(File.file_name == file_name).first()
