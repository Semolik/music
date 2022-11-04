import os
from sqlalchemy.orm import Session
from backend.db.base import CRUDBase
from backend.db.db import get_db
from backend.models.user import File
from pathlib import Path
from backend.core.config import settings


class FileCruds(CRUDBase):
    def delete_file(self, file: File) -> None:
        path = '/'.join([settings.IMAGES_FOLDER if file.type ==
                        'image' else settings.OTHER_FILES_FOLDER, file.file_name])
        if Path(path).exists():
            os.remove(path)
        self.db.delete(file)
        self.db.commit()

    def get_file_by_name(self, file_name: str):
        return self.db.query(File).filter(File.file_name == file_name).first()


file_cruds = FileCruds()
