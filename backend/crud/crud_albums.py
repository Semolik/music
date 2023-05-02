from datetime import datetime
from typing import List
from backend.core.config import settings, env_config
from backend.crud.crud_file import FileCruds
from backend.crud.crud_user import UserCruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.genres import Genre
from backend.models.albums import Album, FavoriteAlbum, AlbumGenre
from backend.models.user import PublicProfile
from sqlalchemy import func


class AlbumsCruds(CRUDBase):

    def get_last_albums(self, page: int, page_size: int) -> List[Album]:
        end = page * page_size
        return self.db.query(Album).filter(Album.is_available).order_by(Album.open_date.desc()).slice(end - page_size, end).all()

    def create_album(self, user_id: int, name: str,  date: datetime, picture: Image | None, genres: List[Genre]):
        db_image = self.create(model=picture) if picture else None
        musician = UserCruds(self.db).get_public_profile(user_id=user_id)
        db_album = Album(musician_id=musician.id, name=name,
                         open_date=date, picture=db_image, genres=genres, uploaded=False)
        return self.create(model=db_album)

    def search_my_albums(self, user_id: int, text: str) -> List[Album]:
        return self.db.query(Album).join(PublicProfile, PublicProfile.user_id == user_id).filter(func.lower(Album.name).contains(text.lower())).all()

    def get_album_count_by_genre_id(self, genre_id: int) -> int:
        return self.db.query(AlbumGenre).filter(AlbumGenre.genre_id == genre_id).count()

    def update_album(self, album: Album, name: str,  date: datetime, genres: List[Genre], image: Image, tracks_ids: List[int]):
        album.name = name
        album.open_date = date
        album.genres = genres
        if image:
            FileCruds(self.db).replace_old_picture(
                model=album, new_picture=image)
        return self.update(model=album)

    def update_album_tracks_order(self, album: Album, tracks_ids: List[int]):
        tracks = album.tracks
        for index, track_id in enumerate(tracks_ids):
            for track in tracks:
                if track.id == track_id:
                    track.track_position = index
        return self.update(model=album)

    def album_belongs_to_user(self, album: Album, user_id: int) -> bool:
        public_profile = self.db.query(PublicProfile).filter(
            PublicProfile.user_id == user_id).first()
        if not public_profile:
            return False
        return album.musician_id == public_profile.id

    def close_uploading(self, album: Album):
        album.uploaded = True
        return self.create(model=album)

    def delete_album(self, album: Album):
        self.delete(model=album)

    def get_album(self, album_id: int) -> Album:
        return self.get(id=album_id, model=Album)

    def get_albums_by_ids(self, albums_ids: List[int]) -> List[Album]:
        return self.db.query(Album).filter(Album.id.in_(albums_ids)).all()

    def get_album_like(self, album: Album, user_id: int) -> FavoriteAlbum:
        return self.db.query(FavoriteAlbum).filter(FavoriteAlbum.album_id == album.id, FavoriteAlbum.user_id == user_id).first()

    def toggle_album_like(self, album: Album, user_id: int):
        like = self.get_album_like(album=album, user_id=user_id)
        if like:
            self.delete(like)
            return False
        else:
            self.create(model=FavoriteAlbum(
                album_id=album.id, user_id=user_id))
            return True

    def get_liked_albums(self, user_id: int, page: int, page_size: int = int(env_config.get('FAVORITE_ALBUMS_LIMIT')), order_by: settings.OrderAlbums = settings.OrderAlbums.date, order: settings.Order = settings.Order.desc) -> List[Album]:
        end = page * page_size
        query = self.db.query(Album).join(FavoriteAlbum, FavoriteAlbum.album_id == Album.id).filter(
            Album.is_available, FavoriteAlbum.user_id == user_id)
        if order_by == settings.OrderAlbums.date:
            order_query = Album.open_date
            query = query.order_by(
                order_query.desc() if order == settings.Order.desc else order_query.asc())
        elif order_by == settings.OrderAlbums.likes:
            order_query = func.count(FavoriteAlbum.date)
            query = query.group_by(Album.id).order_by(
                order_query.desc() if order == settings.Order.desc else order_query.asc())
        elif order_by == settings.OrderAlbums.name:
            order_query = Album.name
            query = query.order_by(
                order_query.desc() if order == settings.Order.desc else order_query.asc())

        return query.slice(end - page_size, end).all()

    def album_is_liked(self, album_id: int, user_id: int) -> bool:
        return self.db.query(FavoriteAlbum).filter(FavoriteAlbum.album_id == album_id, FavoriteAlbum.user_id == user_id).first() is not None

    def get_album_likes_count(self, album: Album) -> int:
        return self.db.query(FavoriteAlbum).filter(FavoriteAlbum.album_id == album.id).count()

    def get_musician_albums(self, musician_id: int, page: int, page_size: int = 100) -> List[Album]:
        end = page * page_size
        return self.db.query(Album).filter(Album.musician_id == musician_id).slice(end - page_size, end).all()
