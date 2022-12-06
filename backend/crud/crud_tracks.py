import os
from pathlib import Path
from backend.crud.crud_file import file_cruds
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.music import Track
from backend.models.user import FavoriteMusicians
from backend.models.music import FavoriteTracks


class TracksCrud(CRUDBase):
    def delete_track(self, track: Track):
        picture = track.picture
        if picture:
            track.picture = None
            file_cruds.delete_image(image=picture)
        path = '/'.join([settings.TRACKS_FOLDER,
                        str(track.id)+settings.SONGS_EXTENTION])
        if Path(path).exists():
            os.remove(path)
        self.db.delete(track)
        self.db.commit()

    def get_track(self, track_id: int):
        return self.get(id=track_id, model=Track)

    def toggle_like_track(self, track_id: int, user_id: int):
        liked = self.get_liked_track_model(track_id=track_id, user_id=user_id)
        if not liked:
            self.create(FavoriteTracks(track_id=track_id, user_id=user_id))
            return True
        else:
            self.delete(model=liked)
            return False

    def get_liked_track_model(self, track_id: int, user_id: int) -> FavoriteTracks | None:
        return self.db.query(FavoriteTracks).filter(
            FavoriteTracks.track_id == track_id and FavoriteTracks.user_id == user_id).first()

    def track_is_liked(self, track_id: int, user_id: int):
        return bool(self.get_liked_track_model(track_id=track_id, user_id=user_id))
