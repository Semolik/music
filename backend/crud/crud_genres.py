from backend.crud.crud_file import FileCruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.genres import Genre


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
