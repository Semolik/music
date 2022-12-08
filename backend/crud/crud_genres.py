from backend.crud.crud_file import FileCruds
from backend.db.base import CRUDBase
from backend.models.music import albums_genres_table
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
            FileCruds(self.db).replace_old_picture(
                model=genre, new_picture=picture)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def detete_genre(self, genre_id: int):
        db_genre = self.get(id=genre_id, model=Genre)
        if not db_genre:
            raise Exception('Жанр не найден')
        rows = self.db.query(albums_genres_table).filter(
            print(albums_genres_table))

        for row in rows:
            self.delete(row)
        return self.delete(model=db_genre)
