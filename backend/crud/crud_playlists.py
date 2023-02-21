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

    def add_tracks_to_playlist(self, db_playlist: Playlist, db_tracks: List[Track], user_id: int):
        for track in db_tracks:
            playlist_track = PlaylistTrack(
                playlist_id=db_playlist.id,
                track_id=track.id,
                user_id=user_id
            )
            self.db.add(playlist_track)
        self.db.commit()
        return db_playlist
