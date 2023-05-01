from backend.crud.crud_file import FileCruds
from backend.db.base import CRUDBase
from backend.models.albums import Album, AlbumGenre, FavoriteAlbum
from backend.models.files import Image
from backend.models.tracks import Track, FavoriteTracks
from backend.models.genres import Genre, LovedGenre
from backend.models.user import PublicProfile, FavoriteMusicians
from sqlalchemy import func, select
from backend.core.config import settings
from sqlalchemy import or_


class GenresCruds(CRUDBase):
    def get_genres(self) -> list[Genre]:
        return self.db.query(Genre).all()

    def get_popular_genres(self, page: int, page_size: int, filter: settings.FilterGenreEnum, current_user_id: int = None) -> list[Genre]:
        end = page * page_size
        query = self.db.query(Genre)
        if filter == settings.FilterGenreEnum.liked:
            query = query.join(LovedGenre, LovedGenre.genre_id == Genre.id)
        else:
            query = query.outerjoin(
                LovedGenre, LovedGenre.genre_id == Genre.id)

        if filter != settings.FilterGenreEnum.all:
            if not current_user_id:
                raise Exception(
                    "current_user_id is None in get_popular_genres")
        if filter == settings.FilterGenreEnum.liked:
            query = query.filter(LovedGenre.user_id == current_user_id)
        elif filter == settings.FilterGenreEnum.not_liked:
            query = query.filter(
                Genre.id.notin_(
                    select(LovedGenre.genre_id).where(
                        LovedGenre.user_id == current_user_id
                    )
                )
            ).filter(LovedGenre.user_id == None)
        return query.slice(end - page_size, end).all()

    def get_liked_genres_ordered_by_likes(self, user_id: int) -> list[Genre]:
        return self.db.query(Genre).join(LovedGenre, LovedGenre.genre_id == Genre.id).filter(LovedGenre.user_id == user_id).order_by(func.count(LovedGenre.genre_id).desc()).all()

    def get_random_genres(self, count: int = settings.SEARCH_GENRE_LIMIT) -> list[Genre]:
        return self.db.query(Genre).order_by(func.random()).limit(count).all()

    def create_genre(self, name: str, picture: Image):
        return self.create(Genre(name=name, picture=picture))

    def get_genre_by_name(self, name: str) -> Genre | None:
        return self.db.query(Genre).filter(Genre.name == name).all()

    def get_genre_by_id(self, id: int) -> Genre | None:
        return self.get(id=id, model=Genre)

    def update_genre(self, name: str, picture: Image, genre: Genre):
        genre.name = name
        if picture:
            FileCruds(self.db).replace_old_picture(
                model=genre, new_picture=picture)
        return self.create(genre)

    def detete_genre(self, genre: Genre):
        return self.delete(model=genre)

    def get_liked_genre_model(self, genre_id: int, user_id: int) -> LovedGenre | None:
        return self.db.query(LovedGenre).filter(
            LovedGenre.genre_id == genre_id, LovedGenre.user_id == user_id).first()

    def toggle_like_genre(self, genre_id: int, user_id: int):
        liked = self.get_liked_genre_model(
            genre_id=genre_id, user_id=user_id)
        if not liked:
            self.create(LovedGenre(
                genre_id=genre_id, user_id=user_id))
            return True
        else:
            self.delete(model=liked)
            return False

    def get_popular_albums_by_genre_id(self, genre_id: int, page: int, page_size: int = settings.POPULAR_TRACKS_LIMIT_ALL) -> list[Album]:
        end = page * page_size
        return self.db.query(Album).join(AlbumGenre, AlbumGenre.album_id == Album.id)\
            .outerjoin(FavoriteAlbum, Album.id == FavoriteAlbum.album_id)\
            .filter(AlbumGenre.genre_id == genre_id, Album.is_available)\
            .group_by(Album.id)\
            .order_by(func.count(FavoriteAlbum.album_id).desc())\
            .slice(end - page_size, end).all()

    def get_popular_tracks_by_genre_id(self, genre_id: int, page: int, page_size: int = settings.POPULAR_TRACKS_LIMIT_ALL) -> list[Track]:
        end = page * page_size
        return self.db.query(Track).join(Album, Album.id == Track.album_id)\
            .join(AlbumGenre, AlbumGenre.album_id == Album.id)\
            .outerjoin(FavoriteTracks, Track.id == FavoriteTracks.track_id)\
            .filter(AlbumGenre.genre_id == genre_id, Track.is_available)\
            .group_by(Track.id)\
            .order_by(func.count(FavoriteTracks.track_id).desc())\
            .slice(end - page_size, end).all()

    def get_popular_musicians_by_genre_id(self, genre_id: int, page: int, page_size: int = settings.POPULAR_MUSICIANS_LIMIT_ALL) -> list[PublicProfile]:
        end = page * page_size
        return self.db.query(PublicProfile).outerjoin(FavoriteMusicians, PublicProfile.id == FavoriteMusicians.musician_id)\
            .join(Album, Album.musician_id == PublicProfile.id)\
            .join(AlbumGenre, AlbumGenre.album_id == Album.id)\
            .filter(AlbumGenre.genre_id == genre_id)\
            .group_by(PublicProfile.id)\
            .order_by(func.count(FavoriteMusicians.musician_id).desc())\
            .slice(end - page_size, end).all()

    def get_new_albums_by_genre_id(self, genre_id: int, page: int, page_size: int = settings.POPULAR_TRACKS_LIMIT_ALL) -> list[Album]:
        end = page * page_size
        return self.db.query(Album).join(AlbumGenre, AlbumGenre.album_id == Album.id)\
            .filter(AlbumGenre.genre_id == genre_id, Album.is_available)\
            .order_by(Album.open_date.desc())\
            .slice(end - page_size, end).all()
