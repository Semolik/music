from datetime import datetime
from backend.crud.crud_user import user_cruds
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.music import Album
from backend.models.user import File


class MusicCrud(CRUDBase):

    def create_album(self, name: str, musician_id: int, date: datetime, picture: File | None):
        db_image = self.create(model=picture) if picture else None
        artist = user_cruds.get_public_profile(user_id=musician_id)
        db_album = Album(artist_id=artist.id, name=name,
                         open_date=date, picture=db_image)
        return self.create(model=db_album)


music_crud = MusicCrud()
