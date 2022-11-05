from datetime import datetime
from typing import List
from backend.crud.crud_user import user_cruds
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.music import Album, Track
from backend.models.user import File


class MusicCrud(CRUDBase):

    def create_album(self, user_id: int, name: str,  date: datetime, picture: File | None):
        db_image = self.create(model=picture) if picture else None
        musician = user_cruds.get_public_profile(user_id=user_id)
        db_album = Album(musician_id=musician.id, name=name,
                         open_date=date, picture=db_image)
        return self.create(model=db_album)

    def get_albums(self, musician_id: int) -> List[Album]:
        return self.db.query(Album).filter(Album.musician_id == musician_id).all()


music_crud = MusicCrud()
