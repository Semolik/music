
from datetime import datetime
from backend.crud.crud_albums import album_cruds
from backend.models.music import Album


def is_album_showed(album: Album, user_id: int):
    if album.open_date > datetime.now() or not album.uploaded:
        if user_id is None or not album_cruds.album_belongs_to_user(album=album, user_id=user_id):
            return False
    return True
