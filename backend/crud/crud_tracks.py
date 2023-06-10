from datetime import datetime, timedelta
from typing import List
from uuid import UUID
from backend.db.base import CRUDBase
from backend.core.config import settings, env_config
from backend.models.albums import Album
from backend.models.playlists import Playlist, PlaylistTrack
from backend.models.tracks import FavoriteTracks, ListenTrackHistoryItem, Track
from backend.schemas.statistics import TrackStats, StatsDay
from sqlalchemy import func


class TracksCrud(CRUDBase):
    def get_track(self, track_id: UUID) -> Track:
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
            FavoriteTracks.track_id == track_id, FavoriteTracks.user_id == user_id).first()

    def track_is_liked(self, track_id: int, user_id: int):
        return bool(self.get_liked_track_model(track_id=track_id, user_id=user_id))

    def get_liked_tracks(self, user_id: int, page: int, page_size: int = int(env_config.get('FAVORITE_TRACKS_LIMIT'))) -> List[Track]:
        end = page * page_size
        start = end - page_size
        return self.db.query(Track).join(FavoriteTracks, FavoriteTracks.track_id == Track.id).join(Album, Album.id == Track.album_id).filter(Track.is_available, FavoriteTracks.user_id == user_id).slice(start, end).all()

    def get_last_listened_tracks(self, user_id: int, page: int, page_size: int = settings.PAGINATION_LIMIT) -> List[ListenTrackHistoryItem]:
        end = page * page_size
        return self.db.query(ListenTrackHistoryItem).filter(ListenTrackHistoryItem.user_id == user_id).slice(end-page_size, end).all()

    def get_last_track_listen(self, track_id: int, user_id: int) -> ListenTrackHistoryItem | None:
        return self.db.query(ListenTrackHistoryItem).filter(ListenTrackHistoryItem.user_id == user_id, ListenTrackHistoryItem.track_id == track_id).first()

    def create_track_listen(self, track_id: int, user_id: int, time: datetime):
        return self.create(ListenTrackHistoryItem(
            track_id=track_id, user_id=user_id, listen_datetime=time))

    def track_is_started_listening(self, last_listened: ListenTrackHistoryItem, time: datetime) -> bool:
        if not last_listened:
            return False
        track: Track = last_listened.track
        target_return_time = time - timedelta(seconds=int(track.duration))
        return (target_return_time - last_listened.listen_datetime) < timedelta(minutes=3)

    def track_is_listened(self, last_listened: ListenTrackHistoryItem, time: datetime) -> bool:
        if not last_listened:
            return False
        track: Track = last_listened.track
        # Время, когда трек должен был начаться если прослушивание закончилось во время (time)
        target_return_time = time - timedelta(seconds=int(track.duration))
        return target_return_time > last_listened.listen_datetime if target_return_time - last_listened.listen_datetime < timedelta(minutes=3) else False

    def add_track_to_history(self, track_id: int, user_id: int, time: datetime):
        last_listened = self.get_last_track_listen(
            user_id=user_id, track_id=track_id)
        if last_listened and not last_listened.listened:
            is_listened = self.track_is_listened(
                last_listened=last_listened, time=time)
            if not is_listened:
                return
            last_listened.listen_datetime = datetime.now()

            return self.update(model=last_listened)
        return self.create(ListenTrackHistoryItem(
            track_id=track_id, user_id=user_id, listen_datetime=time))

    def get_popular_tracks(self,  start_date: datetime = None, end_date: datetime = None, page: int = 1, page_size: int = settings.POPULAR_TRACKS_LIMIT) -> List[Track]:
        end = page * page_size
        query = self.db.query(Track).join(ListenTrackHistoryItem, ListenTrackHistoryItem.track_id == Track.id).join(Album, Album.id == Track.album_id).filter(
            Track.is_available, ListenTrackHistoryItem.listened == True)
        if start_date:
            query = query.filter(
                ListenTrackHistoryItem.listen_datetime >= start_date)
        if end_date:
            query = query.filter(
                ListenTrackHistoryItem.listen_datetime <= end_date)
        return query.group_by(Track.id).order_by(func.count(ListenTrackHistoryItem.id).desc()).slice(end-page_size, end).all()

    def get_track_statistics(self, track: Track) -> TrackStats:
        total_count = self.db.query(ListenTrackHistoryItem).filter(
            ListenTrackHistoryItem.track_id == track.id, ListenTrackHistoryItem.listened == True).count()
        now = datetime.now()
        days = []
        week_start = now - timedelta(days=now.weekday())
        for i in range(7):
            day_start = week_start + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            count = self.db.query(ListenTrackHistoryItem).filter(
                ListenTrackHistoryItem.listened == True,
                ListenTrackHistoryItem.track_id == track.id,
                ListenTrackHistoryItem.listen_datetime >= day_start,
                ListenTrackHistoryItem.listen_datetime <= day_end
            ).count()
            days.append(
                StatsDay(day=day_start, count=count, listens=count)
            )
        return TrackStats(
            track_id=track.id,
            total_listens=total_count,
            calendar=days
        )

    def get_my_track_playlists(self, track_id: int, user_id: int) -> List[Playlist]:
        return self.db.query(Playlist).join(PlaylistTrack, PlaylistTrack.playlist_id == Playlist.id).filter(
            PlaylistTrack.track_id == track_id, Playlist.user_id == user_id).all()
