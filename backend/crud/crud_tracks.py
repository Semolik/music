from datetime import datetime, timedelta
from typing import List
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.tracks import FavoriteTracks, ListenTrackHistoryItem, Track
from backend.schemas.statistics import TrackStats, StatsDay


class TracksCrud(CRUDBase):
    def get_track(self, track_id: int) -> Track:
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

    def get_liked_tracks(self, user_id: int, page: int) -> List[Track]:
        end = page * settings.PAGINATION_LIMIT
        return self.db.query(Track).join(FavoriteTracks).filter(FavoriteTracks.user_id == user_id).slice(end-settings.PAGINATION_LIMIT, end).all()

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
