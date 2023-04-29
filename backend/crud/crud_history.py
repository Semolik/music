from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_musician import MusicianCrud
from backend.crud.crud_playlists import PlaylistsCrud
from backend.db.base import CRUDBase
from backend.models.albums import Album,  ListenAlbumHistoryItem
from backend.models.playlists import Playlist, ListenPlaylistHistoryItem
from backend.models.tracks import Track, ListenTrackHistoryItem
from backend.models.user import PublicProfile, ListenMusicianHistoryItem
from backend.core.config import env_config
from sqlalchemy import desc,  literal_column, Text, cast,  union_all
import uuid

from backend.schemas.history import HistoryItem


class HistoryCrud(CRUDBase):
    def get_history(self, user_id: int, limit: int = int(env_config.get('HISTORY_ALL_LIMIT'))) -> list[HistoryItem]:
        label_resource_type = "resource_type"
        label_listen_date = "listen_date"
        label_id = "id"
        album_resource_type = 'album'
        playlist_resource_type = 'playlist'
        musician_resource_type = 'musician'
        history_item_id = 'history_item_id'

        q1 = (self.db.query(
            cast(Album.id, Text).label(label_id),
            literal_column(f"'{album_resource_type}'").label(
                label_resource_type),
            ListenAlbumHistoryItem.listen_datetime.label(
                label_listen_date),
            ListenAlbumHistoryItem.id.label(history_item_id))
            .select_from(ListenAlbumHistoryItem)
            .join(Album, ListenAlbumHistoryItem.album_id == Album.id)
            .filter(ListenAlbumHistoryItem.user_id == user_id)
            .distinct(Album.id)
        )

        q2 = (
            self.db.query(
                cast(Playlist.id, Text).label(label_id),
                literal_column(f"'{playlist_resource_type}'").label(
                    label_resource_type),
                ListenPlaylistHistoryItem.listen_datetime.label(
                    label_listen_date),
                ListenPlaylistHistoryItem.id.label(history_item_id)
            )
            .select_from(ListenPlaylistHistoryItem)
            .join(Playlist, ListenPlaylistHistoryItem.playlist_id == Playlist.id)
            .filter(ListenPlaylistHistoryItem.user_id == user_id)
            .distinct(Playlist.id)
        )

        q3 = (self.db.query(
            cast(PublicProfile.id, Text).label(label_id),
            literal_column(f"'{musician_resource_type}'").label(
                label_resource_type),
            ListenMusicianHistoryItem.listen_datetime.label(
                label_listen_date),
            ListenMusicianHistoryItem.id.label(history_item_id))
            .select_from(ListenMusicianHistoryItem)
            .join(PublicProfile, ListenMusicianHistoryItem.musician_id == PublicProfile.id)
            .filter(ListenMusicianHistoryItem.user_id == user_id)
            .distinct(PublicProfile.id)
        )

        query = union_all(q1, q2, q3).alias("history")
        query_result = self.db.query(
            query.c.id,
            query.c.resource_type,
            query.c.listen_date,
            query.c.history_item_id
        ).order_by(desc(query.c.listen_date)).limit(limit).all()
        albums = []
        playlists = []
        musicians = []
        for index, item in enumerate(query_result):
            value = (item.id, index, item.listen_date, item.history_item_id)
            if item.resource_type == album_resource_type:
                albums.append(value)
            elif item.resource_type == playlist_resource_type:
                playlists.append(value)
            elif item.resource_type == musician_resource_type:
                musicians.append(value)

        db_albums = AlbumsCruds(self.db).get_albums_by_ids(
            [int(item[0]) for item in albums])
        result_albums = []
        for album in db_albums:
            for item in albums:
                if item[0] == str(album.id):
                    album.current_user_id = user_id
                    result_albums.append(
                        (item[0], album_resource_type, item[2], item[3], album))
                    break

        db_playlists = PlaylistsCrud(self.db).get_playlists_by_ids(
            [uuid.UUID(item[0]) for item in playlists])
        result_playlists = []
        for playlist in db_playlists:
            for item in playlists:
                if item[0] == str(playlist.id):
                    playlist.current_user_id = user_id
                    result_playlists.append(
                        (item[0], playlist_resource_type, item[2], item[3], playlist))
                    break

        db_musicians = MusicianCrud(self.db).get_musicians_by_ids(
            [int(item[0]) for item in musicians])
        result_musicians = []
        for musician in db_musicians:
            for item in musicians:
                if item[0] == str(musician.id):
                    musician.current_user_id = user_id
                    result_musicians.append(
                        (item[0], musician_resource_type, item[2], item[3], musician))
                    break
        all_items = result_albums + result_playlists + result_musicians
        all_items.sort(key=lambda x: x[2], reverse=True)
        return [HistoryItem(id=int(item[3]), type=item[1],  info=item[4]) for item in all_items]

    def get_tracks_history(self, user_id: int, page: int = 1, page_size: int = int(env_config.get('HISTORY_ALL_TRACKS_LIMIT'))):
        end = page * page_size
        start = end - page_size
        query = (
            self.db.query(Track, ListenTrackHistoryItem)
            .select_from(ListenTrackHistoryItem)
            .join(Track, ListenTrackHistoryItem.track_id == Track.id)
            .filter(ListenTrackHistoryItem.user_id == user_id)
            .order_by(desc(ListenTrackHistoryItem.listen_datetime))
            .slice(start, end)
        )
        return [item[0] for item in query.all()]
