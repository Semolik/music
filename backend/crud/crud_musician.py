from typing import List
from backend.db.base import CRUDBase
from backend.models.tracks import FavoriteTracks, Track, ListenTrackHistoryItem
from backend.models.albums import Album, FavoriteAlbum
from backend.models.user import FavoriteMusicians, PublicProfile
from backend.core.config import env_config, settings
from sqlalchemy import and_, func


class MusicianCrud(CRUDBase):

    def musician_is_liked(self, musician_id: int, user_id: int):
        return bool(self.get_liked_musician_model(musician_id=musician_id, user_id=user_id))

    def get_liked_musician_model(self, musician_id: int, user_id: int) -> FavoriteMusicians | None:
        return self.db.query(FavoriteMusicians).filter(
            FavoriteMusicians.musician_id == musician_id, FavoriteMusicians.user_id == user_id).first()

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

    def get_musician_likes_count(self, musician_id: int) -> int:
        return self.db.query(FavoriteMusicians).filter(
            FavoriteMusicians.musician_id == musician_id).count()

    def get_musicians_by_ids(self, musician_ids: List[int]) -> List[PublicProfile]:
        return self.db.query(PublicProfile).filter(PublicProfile.id.in_(musician_ids)).all()

    def get_random_musician_profiles(self, limit: int = settings.AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT) -> List[PublicProfile]:
        return self.db.query(PublicProfile).order_by(func.random()).limit(limit).all()

    def get_popular_musician_profiles(self, page: int, page_size: int = settings.SEARCH_MUSICIAN_LIMIT) -> List[PublicProfile]:
        end = page * page_size
        return self.db.query(PublicProfile).outerjoin(FavoriteMusicians, FavoriteMusicians.musician_id == PublicProfile.id).group_by(PublicProfile.id).order_by(
            func.count(FavoriteMusicians.musician_id).desc()).slice(start=(end - page_size), stop=end).all()

    def get_musician_albums(self, musician_id: int, page: int = 1, page_size: int = settings.ALBUM_PAGE_COUNT_ALL) -> List[Album]:
        end = page * page_size
        return self.db.query(Album).filter(Album.musician_id == musician_id).order_by(Album.open_date.desc()).slice(
            start=(end - page_size), stop=end).all()

    def get_all_musician_albums(self, musician_id: int, limit: int = None) -> List[Album]:
        query = self.db.query(Album).filter(
            Album.musician_id == musician_id).order_by(Album.open_date.desc())
        return query.limit(limit).all() if limit else query.all()

    def get_popular_musician_tracks(self, musician_id: int, page: int = 1, page_size: int = settings.POPULAR_TRACKS_LIMIT_ALL) -> List[Track]:
        end = page * page_size
        return self.db.query(Track)\
            .join(Album, and_(Album.id == Track.album_id, Album.is_available, Album.musician_id == musician_id))\
            .outerjoin(FavoriteTracks, FavoriteTracks.track_id == Track.id)\
            .group_by(Track.id) \
            .order_by(func.count().desc())\
            .slice(start=(end - page_size), stop=end)\
            .all()

    def search_popular_musician_tracks(self, musician_id: int, search: str, page: int = 1, page_size: int = settings.POPULAR_TRACKS_LIMIT_ALL) -> List[Track]:
        end = page * page_size
        return self.db.query(Track)\
            .join(Album, Album.id == Track.album_id)\
            .filter(Track.artist_id == musician_id, Track.is_available, Track.name.ilike(f'%{search}%'))\
            .join(FavoriteTracks, FavoriteTracks.track_id == Track.id, isouter=True)\
            .group_by(Track.id) \
            .order_by(func.count().desc())\
            .slice(start=(end - page_size), stop=end)\
            .all()

    def get_popular_musician_albums(self, musician_id: int, page: int = 1, page_size: int = settings.ALBUM_PAGE_COUNT_ALL) -> List[Album]:
        end = page * page_size
        return self.db.query(Album)\
            .filter(Album.musician_id == musician_id, Album.is_available)\
            .join(FavoriteAlbum, FavoriteAlbum.album_id == Album.id, isouter=True)\
            .group_by(Album.id) \
            .order_by(func.count().desc())\
            .slice(start=(end - page_size), stop=end)\
            .all()

    def get_liked_musicians(self, user_id: int, page: int = 1, page_size: int = int(env_config.get('FAVORITE_MUSICIANS_LIMIT'))) -> List[PublicProfile]:
        end = page * page_size
        return self.db.query(PublicProfile).join(FavoriteMusicians, FavoriteMusicians.musician_id == PublicProfile.id).filter(
            FavoriteMusicians.user_id == user_id).order_by(PublicProfile.name.asc()).slice(
            start=(end - page_size), stop=end).all()
