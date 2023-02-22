from typing import List
from uuid import UUID
from backend.db.base import CRUDBase
from backend.models.albums import Album
from backend.models.playlists import Playlist, PlaylistTrack, FavoritePlaylist
from backend.models.tracks import Track


class PlaylistsCrud(CRUDBase):
    def get_playlist_info(self, playlist_id: UUID) -> Playlist:
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()

    def update_playlist(self, playlist: Playlist, name: str, description: str, private: bool) -> Playlist:
        playlist.name = name
        playlist.description = description
        playlist.private = private
        return self.update(playlist)

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

    def get_tracks_by_playlist_id(self, playlist_id: UUID, user_id: int) -> List[Track]:
        return self.db.query(Track).join(PlaylistTrack, Album).filter(Album.is_available, PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.user_id == user_id).all()

    def get_playlist_track(self, playlist_id: UUID, track_id: UUID, user_id: int) -> PlaylistTrack:
        return self.db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id, PlaylistTrack.user_id == user_id).first()

    def add_track_to_playlist(self, playlist_id: UUID, track_id: UUID, user_id: int) -> PlaylistTrack:
        return self.create(
            PlaylistTrack(
                playlist_id=playlist_id,
                track_id=track_id,
                user_id=user_id
            )
        )

    def get_favorite_playlist(self, user_id: int, playlist_id: UUID) -> FavoritePlaylist:
        return self.db.query(FavoritePlaylist).filter(FavoritePlaylist.user_id == user_id, FavoritePlaylist.playlist_id == playlist_id).first()

    def toggle_like_playlist(self, user_id: int, playlist_id: UUID) -> FavoritePlaylist:
        favorite_playlist = self.get_favorite_playlist(user_id, playlist_id)
        if favorite_playlist:
            self.delete(favorite_playlist)
            return False
        else:
            self.create(
                FavoritePlaylist(
                    user_id=user_id,
                    playlist_id=playlist_id
                )
            )
            return True
