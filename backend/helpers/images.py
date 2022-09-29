import io
import shutil
from fastapi import UploadFile, HTTPException
from PIL import Image
import uuid
from core.config import settings


def save_image(upload_file: UploadFile):
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
    