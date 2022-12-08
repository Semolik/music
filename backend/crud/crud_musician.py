from datetime import datetime
import os
from pathlib import Path
from typing import List
from backend.crud.crud_file import FileCruds
from backend.crud.crud_user import UserCruds
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.files import Image
from backend.models.music import Album, Genre, Track
from backend.models.user import FavoriteMusicians


class MusicianCrud(CRUDBase):

    def musician_is_liked(self, musician_id: int, user_id: int):
        return bool(self.get_liked_musician_model(musician_id=musician_id, user_id=user_id))

    def get_liked_musician_model(self, musician_id: int, user_id: int) -> FavoriteMusicians | None:
        return self.db.query(FavoriteMusicians).filter(
            FavoriteMusicians.musician_id == musician_id and FavoriteMusicians.user_id == user_id).first()

    def toggle_like_musician(self, musician_id: int, user_id: int):
        liked = self.get_liked_musician_model(
            musician_id=musician_id, user_id=user_id)
        if not liked:
            self.create(FavoriteMusicians(
                musician_id=musician_id, user_id=user_id))
            return True
        else:
            self.delete(model=liked)
            return False

    def get_musician_albums(self, musician_id: int) -> List[Album]:
        return self.db.query(Album).filter(Album.musician_id == musician_id).all()
