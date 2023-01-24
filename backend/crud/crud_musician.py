from typing import List
from backend.db.base import CRUDBase
from backend.models.music import Album, Track, FavoriteTracks
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

    def get_musician_albums(self, musician_id: int, page: int = 1, page_size: int = 10) -> List[Album]:
        end = page * page_size
        return self.db.query(Album).filter(Album.musician_id == musician_id).order_by(Album.open_date.desc()).slice(
            start=(end - page_size), stop=end).all()

    def get_all_musician_albums(self, musician_id: int, limit: int = None) -> List[Album]:
        query = self.db.query(Album).filter(
            Album.musician_id == musician_id).order_by(Album.open_date.desc())
        return query.limit(limit).all() if limit else query.all()
