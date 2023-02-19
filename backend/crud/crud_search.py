

from backend.core.config import settings
from backend.db.base import CRUDBase
from backend.models.albums import Album
from sqlalchemy import func
from backend.models.user import PublicProfile
from backend.models.tracks import Track
from backend.models.clips import Clip


class SearchCrud(CRUDBase):
    def search_albums_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_ALBUM_LIMIT):
        return self.db.query(Album).filter(Album.is_available, func.lower(Album.name).contains(name.lower())).limit(limit).all()

    def search_tracks_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_TRACK_LIMIT):
        return self.db.query(Track).join(Album).filter(Album.is_available, func.lower(Track.name).contains(name.lower())).limit(limit).all()

    def search_musicians_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT):
        return self.base_search_by_name(name=name, limit=limit, model=PublicProfile)

    def search_clips_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_CLIP_LIMIT):
        return self.base_search_by_name(name=name, limit=limit, model=Clip)

    def base_search_by_name(self, model, name: str, limit: int):
        return self.db.query(model).filter(func.lower(model.name).contains(name.lower())).limit(limit).all()
