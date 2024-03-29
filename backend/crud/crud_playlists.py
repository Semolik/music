from typing import List
from uuid import UUID
from backend.db.base import CRUDBase
from backend.models.albums import Album
from backend.models.playlists import Playlist, PlaylistTrack, FavoritePlaylist
from backend.models.tracks import Track
from sqlalchemy import or_
from backend.core.config import env_config


class PlaylistsCrud(CRUDBase):
    def get_playlist_info(self, playlist_id: UUID) -> Playlist:
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()

    def get_playlists_by_ids(self, playlist_ids: List[UUID]) -> List[Playlist]:
        return self.db.query(Playlist).filter(Playlist.id.in_(playlist_ids)).all()

    def update_playlist(self, playlist: Playlist, name: str, description: str, private: bool) -> Playlist:
        playlist.name = name
        playlist.description = description
        playlist.private = private
        return self.update(playlist)

    def is_playlist_liked(self, user_id: int, playlist_id: UUID) -> bool:
        return self.db.query(FavoritePlaylist).filter(FavoritePlaylist.user_id == user_id, FavoritePlaylist.playlist_id == playlist_id).first() is not None

    def get_playlists_by_user_id(self, owner_id: int, user_id: int, order_by: str, order_orientation: str, owned_only: bool, private: bool, page: int, page_size=int(env_config.get('USER_PLAYLISTS_LIMIT'))) -> List[Playlist]:
        query = self.db.query(Playlist).outerjoin(
            FavoritePlaylist, FavoritePlaylist.playlist_id == Playlist.id)
        if owned_only:
            query = query.filter(Playlist.user_id == owner_id)
        else:
            query = query.filter(or_(
                Playlist.user_id == owner_id, FavoritePlaylist.user_id == user_id))
        if private:
            query = query.filter(Playlist.private == True,
                                 Playlist.user_id == owner_id)
        elif private is False:
            query = query.filter(Playlist.private == False)
        query = query.group_by(Playlist.id)
        if order_by == 'created_at':
            order_column = Playlist.created_at
        elif order_by == 'name':
            order_column = Playlist.name
        else:
            order_column = None

        if order_column is not None:
            order_method = getattr(order_column, order_orientation)
            query = query.order_by(order_method())

        if owner_id != user_id:
            query = query.filter(Playlist.private == False)
        end = page * page_size
        return query.slice(end-page_size, page_size).all()

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
                track_id=track_id
            )
            self.db.add(playlist_track)
        self.db.commit()
        return playlist

    def get_tracks_by_playlist_id(self, playlist_id: UUID, user_id: int) -> List[Track]:
        return self.db.query(Track).join(PlaylistTrack, PlaylistTrack.track_id == Track.id)\
            .join(Playlist, Playlist.id == PlaylistTrack.playlist_id)\
            .join(Album, Album.id == Track.album_id)\
            .filter(Album.is_available, PlaylistTrack.playlist_id == playlist_id, Playlist.user_id == user_id).all()

    def get_playlist_track(self, playlist_id: UUID, track_id: UUID, user_id: int) -> PlaylistTrack:
        return self.db.query(PlaylistTrack).join(Playlist, PlaylistTrack.playlist_id == Playlist.id).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id, Playlist.user_id == user_id).first()

    def add_track_to_playlist(self, playlist_id: UUID, track_id: UUID) -> PlaylistTrack:
        return self.create(
            PlaylistTrack(
                playlist_id=playlist_id,
                track_id=track_id
            )
        )

    def get_favorite_playlist(self, user_id: int, playlist_id: UUID) -> FavoritePlaylist:
        return self.db.query(FavoritePlaylist).filter(FavoritePlaylist.user_id == user_id, FavoritePlaylist.playlist_id == playlist_id).first()

    def playlist_is_liked(self, user_id: int, playlist_id: UUID) -> bool:
        return self.get_favorite_playlist(user_id, playlist_id) is not None

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
