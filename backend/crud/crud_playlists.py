from typing import List
from uuid import UUID
from backend.db.base import CRUDBase
from backend.models.playlists import Playlist, PlaylistTrack, FavoritePlaylist
from backend.models.tracks import Track


class PlaylistsCrud(CRUDBase):
    def get_playlist_info(self, playlist_id: UUID) -> Playlist:
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()

    def create_playlist(self, name: str, description: str, user_id: int, private: bool, tracks_ids: List[UUID]):
        playlist = self.create(
            Playlist(
                name=name,
                description=description,
                user_id=user_id,
                private=private
            )
        )
        for track_id in tracks_ids:
            playlist_track = PlaylistTrack(
                playlist_id=playlist.id,
                track_id=track_id,
                user_id=user_id
            )
            self.db.add(playlist_track)
        self.db.commit()
        return playlist

    def get_tracks_by_playlist_id(self, playlist_id: UUID, user_id: int):
        return self.db.query(PlaylistTrack).filter(PlaylistTrack.track.is_avaible, PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.user_id == user_id).all()

    def add_track_to_playlist(self, playlist_id: UUID, track_id: UUID, user_id: int):
        return self.create(
            PlaylistTrack(
                playlist_id=playlist_id,
                track_id=track_id,
                user_id=user_id
            )
        )
