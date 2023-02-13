from backend.crud.crud_file import FileCruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.genres import Genre, LovedGenre
from backend.models.user import User


class GenresCruds(CRUDBase):
    def get_genres(self) -> list[Genre]:
        return self.db.query(Genre).all()

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
