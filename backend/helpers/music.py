from backend.helpers.images import set_picture
from backend.helpers.users import get_public_profile_as_dict
from backend.models.music import Album, Track
from backend.schemas.track import UploadTrackForm
from backend.crud.crud_user import user_cruds
from backend.db.base import crud_base
from pydub import AudioSegment
from fastapi import UploadFile, HTTPException
from pathlib import Path
import uuid
import shutil
from backend.core.config import settings
from backend.models.user import File
import io


def save_track(upload_file: UploadFile, picture: File, user_id: int, track: UploadTrackForm):
    originalFileName = upload_file.filename
    uuid_filename = str(uuid.uuid4())
    buf = io.BytesIO()
    shutil.copyfileobj(upload_file.file, buf)
    buf.seek(0)
    fileName = uuid_filename + settings.SONGS_EXTENTION
    try:
        segment = AudioSegment.from_file(buf)
        segment.export('/'.join([settings.TRACKS_FOLDER, fileName]),
                       format=settings.SONGS_EXTENTION.replace('.', ''))
        db_file = crud_base.create(
            model=File(
                file_name=fileName,
                original_file_name=originalFileName,
                user_id=user_id,
                type='track'
            )
        )
        artist_public_profile = user_cruds.get_public_profile(user_id=user_id)
        db_picture = crud_base.create(picture) if picture else None
        db_track = crud_base.create(
            Track(
                artist_id=artist_public_profile.id,
                name=track.name,
                feat=track.feat,
                open_date=track.date,
                duration=segment.duration_seconds,
                file=db_file,
                album_id=track.album_id,
                picture=db_picture,
                genres=track.genres
            )
        )
        return db_track
    except:
        raise HTTPException(status_code=500, detail="поврежденный файл")


def set_album_info(db_album: Album, user_id: int | None = None):
    db_album_obj = db_album.as_dict()
    db_album_obj['year'] = db_album.open_date.year
    db_album_obj['musician'] = get_public_profile_as_dict(
        user_id=user_id, musician_id=db_album.musician_id)
    db_album_obj = set_picture(db_album_obj, db_album.picture)
    return db_album_obj
