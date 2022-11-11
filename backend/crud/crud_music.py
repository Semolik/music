from datetime import datetime
from typing import List
from backend.crud.crud_user import user_cruds
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.music import Album, Genre, Track
from backend.models.user import File


class MusicCrud(CRUDBase):

    def create_album(self, user_id: int, name: str,  date: datetime, picture: File | None, genres: List[Genre]):
        db_image = self.create(model=picture) if picture else None
        musician = user_cruds.get_public_profile(user_id=user_id)
        db_album = Album(musician_id=musician.id, name=name,
                         open_date=date, picture=db_image, genres=genres)
        return self.create(model=db_album)

    def get_musician_albums(self, musician_id: int) -> List[Album]:
        return self.db.query(Album).filter(Album.musician_id == musician_id).all()

    def get_album(self, album_id: int) -> Album:
        return self.get(album_id, Album)

    def get_album_tracks(self, album_id: int) -> List[Track]:
        return self.db.query(Track).filter(Track.album_id == album_id).all()

    def get_genres(self):
        return self.db.query(Genre).all()

    def create_genre(self, name: str, picture: File):
        return self.create(Genre(name=name, picture=self.create(picture)))

    def get_genre_by_name(self, name: str) -> Genre | None:
        return self.db.query(Genre).filter(Genre.name == name).all()

    def get_genre_by_id(self, id: int) -> Genre | None:
        return self.get(id=id, model=Genre)

    def update_genre(self, name: str, picture: File, genre: Genre):
        genre.name = name
        if picture:
            genre.picture = self.create(picture)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def detete_genre(self, genre_id: int):
        return self.db.query(Genre).filter(Genre.id == genre_id).delete()


music_crud = MusicCrud()
