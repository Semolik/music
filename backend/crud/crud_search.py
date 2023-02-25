

from uuid import UUID
from backend.core.config import settings
from backend.crud.crud_musician import MusicianCrud
from backend.db.base import CRUDBase
from backend.models.albums import Album, FavoriteAlbum
from sqlalchemy import Text, cast, func, union_all
from backend.models.playlists import Playlist
from backend.models.user import PublicProfile, FavoriteMusicians
from backend.models.tracks import Track, FavoriteTracks
from backend.models.clips import Clip
from sqlalchemy import desc, func, literal_column
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_user import UserCruds
from backend.crud.crud_playlists import PlaylistsCrud
from backend.schemas.search import AllSearchItem, SearchAlbum, SearchMusician, SearchPlaylist, SearchTrack
from sqlalchemy import or_


class SearchCrud(CRUDBase):
    def search_albums_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_ALBUM_LIMIT) -> list[Album]:
        return self.db.query(Album).filter(Album.is_available, func.lower(Album.name).contains(name.lower())).limit(limit).all()

    def search_tracks_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_TRACK_LIMIT) -> list[Track]:
        return self.db.query(Track).join(Album).filter(Album.is_available, func.lower(Track.name).contains(name.lower())).limit(limit).all()

    def search_musicians_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT) -> list[PublicProfile]:
        return self.base_search_by_name(name=name, limit=limit, model=PublicProfile)

    def search_clips_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_CLIP_LIMIT) -> list[Clip]:
        return self.base_search_by_name(name=name, limit=limit, model=Clip)

    def base_search_by_name(self, model, name: str, limit: int):
        return self.db.query(model).filter(func.lower(model.name).contains(name.lower())).limit(limit).all()

    def search_playlists_by_name(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_PLAYLIST_LIMIT, user_id: int = None) -> list[Playlist]:
        return self.db.query(Playlist).filter(or_(Playlist.user_id == user_id, Playlist.private == False)).filter(func.lower(Playlist.name).contains(name.lower())).limit(limit).all()

    def search_all_by_name_sorted_by_likes(self, name: str, limit: int = settings.AUTOCOMPLETE_SEARCH_ALL_LIMIT, user_id: int = None):
        label_num_likes = "num_likes"
        label_resource_type = "resource_type"
        label_id = "id"
        album_resource_type = 'album'
        track_resource_type = 'track'
        playlist_resource_type = 'playlist'
        musician_resource_type = 'musician'
        q1 = self.db.query(
            cast(Album.id, Text).label(label_id),
            func.count(FavoriteAlbum.album_id).label(label_num_likes),
            literal_column(f"'{album_resource_type}'").label(
                label_resource_type)
        ).join(
            FavoriteAlbum, Album.id == FavoriteAlbum.album_id, isouter=True
        ).filter(
            Album.is_available,
            func.lower(Album.name).contains(name.lower())
        ).group_by(Album.id)

        q2 = self.db.query(
            cast(PublicProfile.id, Text).label(label_id),
            func.count(FavoriteMusicians.musician_id).label(label_num_likes),
            literal_column(f"'{musician_resource_type}'").label(
                label_resource_type)
        ).join(
            FavoriteMusicians, PublicProfile.id == FavoriteMusicians.musician_id, isouter=True
        ).filter(
            func.lower(PublicProfile.name).contains(name.lower())
        ).group_by(PublicProfile.id)

        q3 = self.db.query(
            cast(Track.id, Text).label(label_id),
            func.count(FavoriteTracks.track_id).label(label_num_likes),
            literal_column(f"'{track_resource_type}'").label(
                label_resource_type)
        ).join(Album, Track.album_id == Album.id).join(
            FavoriteTracks, Track.id == FavoriteTracks.track_id, isouter=True
        ).filter(
            Album.is_available,
            func.lower(Track.name).contains(name.lower())
        ).group_by(Track.id)

        q4 = self.db.query(
            cast(Playlist.id, Text).label(label_id),
            literal_column("0").label(label_num_likes),
            literal_column(f"'{playlist_resource_type}'").label(
                label_resource_type)
        ).filter(or_(Playlist.user_id == user_id, Playlist.private == False)).filter(
            func.lower(Playlist.name).contains(name.lower())
        ).group_by(Playlist.id)

        query = union_all(q1, q2, q3, q4)
        query_result = self.db.query(
            getattr(query.c, label_id),
            getattr(query.c, label_num_likes),
            getattr(query.c, label_resource_type),
        ).order_by(desc(label_num_likes)).limit(limit).all()
        results = []
        for query_item in query_result:
            resource_type = getattr(query_item, label_resource_type)
            likes_count = getattr(query_item, label_num_likes)
            model_schema = None
            if resource_type == track_resource_type:
                model_schema = SearchTrack.from_orm(TracksCrud(self.db).get_track(
                    track_id=UUID(query_item.id)))
                if user_id:
                    model_schema.liked = TracksCrud(self.db).track_is_liked(
                        track_id=UUID(query_item.id), user_id=user_id)
            elif resource_type == album_resource_type:
                model_schema = SearchAlbum.from_orm(AlbumsCruds(self.db).get_album(
                    album_id=int(query_item.id)
                ))
                if user_id:
                    model_schema.liked = AlbumsCruds(self.db).album_is_liked(
                        album_id=int(query_item.id), user_id=user_id)
            elif resource_type == musician_resource_type:
                model_schema = SearchMusician.from_orm(UserCruds(self.db).get_public_profile_by_id(
                    id=int(query_item.id)))
                if user_id:
                    model_schema.liked = MusicianCrud(self.db).musician_is_liked(
                        musician_id=int(query_item.id), user_id=user_id)
            elif resource_type == playlist_resource_type:
                model_schema = SearchPlaylist.from_orm(PlaylistsCrud(self.db).get_playlist_info(
                    playlist_id=UUID(query_item.id)))
                if user_id:
                    model_schema.liked = PlaylistsCrud(self.db).playlist_is_liked(
                        playlist_id=UUID(query_item.id), user_id=user_id)
            if model_schema:
                results.append(AllSearchItem(
                    type=resource_type,
                    info=model_schema,
                    likes_count=likes_count
                ))
        return results
