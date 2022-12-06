from backend.crud.crud_file import file_cruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.music import Genre


class GenresCruds(CRUDBase):
    def get_genres(self):
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
            file_cruds.replace_old_picture(model=genre, new_picture=picture)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def detete_genre(self, genre_id: int):
        return self.db.query(Genre).filter(Genre.id == genre_id).delete()


genres_cruds = GenresCruds()
