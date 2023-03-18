from backend.crud.crud_file import FileCruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.genres import Genre, LovedGenre
from sqlalchemy import func
from backend.core.config import settings


class GenresCruds(CRUDBase):
    def get_genres(self) -> list[Genre]:
        return self.db.query(Genre).all()

    def get_popular_genres(self, page: int, page_size: int, filter: settings.FilterGenreEnum, current_user_id: int = None) -> list[Genre]:
        end = page * page_size
        query = self.db.query(Genre)
        if filter == settings.FilterGenreEnum.liked:
            query = query.join(LovedGenre)
        else:
            query = query.outerjoin(LovedGenre)
        query = query.group_by(Genre.id).order_by(
            func.count(LovedGenre.genre_id).desc())
        if filter != settings.FilterGenreEnum.all:
            if not current_user_id:
                raise Exception(
                    "current_user_id is None in get_popular_genres")
        if filter == settings.FilterGenreEnum.liked:
            query = query.filter(LovedGenre.user_id == current_user_id)
        elif filter == settings.FilterGenreEnum.not_liked:
            query = query.filter(LovedGenre.user_id.is_(None))

        return query.slice(end - page_size, end).all()

    def get_liked_genres_ordered_by_likes(self, user_id: int) -> list[Genre]:
        return self.db.query(Genre).join(LovedGenre).filter(LovedGenre.user_id == user_id).order_by(func.count(LovedGenre.genre_id).desc()).all()

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
