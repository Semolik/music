import os
from sqlalchemy.orm import Session
from models.user import File
from pathlib import Path
from core.config import settings


class FileCruds:
    def __init__(self, db: Session) -> None:
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

