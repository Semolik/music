
from datetime import datetime
from backend.crud.crud_albums import AlbumsCruds
from backend.models.music import Album
from sqlalchemy.orm import Session


def is_album_showed(db: Session, album: Album, user_id: int):
    if album.open_date > datetime.now() or not album.uploaded:
        if user_id is None or not AlbumsCruds(db).album_belongs_to_user(album=album, user_id=user_id):
            return False
    return True
