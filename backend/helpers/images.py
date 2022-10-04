import io
import shutil
from fastapi import UploadFile, HTTPException, Depends
from PIL import Image
import uuid
from models.user import File, User
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
        fileName = '.'.join([str(uuid.uuid4()), 'png'])
        image.save('/'.join([settings.IMAGES_FOLDER, fileName]))
    except:
        raise HTTPException(status_code=500, detail="поврежденный файл")
    db_file = File(file_name=fileName, user_id=user.id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
