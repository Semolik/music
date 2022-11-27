from datetime import datetime
import os
from pathlib import Path
from typing import List
from backend.crud.crud_file import file_cruds
from backend.crud.crud_user import user_cruds
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.music import Album, Clip, Genre, Track
from backend.models.user import FavoriteMusicians, File
from backend.models.music import FavoriteTracks


class MusicCrud(CRUDBase):

    def create_album(self, user_id: int, name: str,  date: datetime, picture: File | None, genres: List[Genre]):
        db_image = self.create(model=picture) if picture else None
        musician = user_cruds.get_public_profile(user_id=user_id)
        db_album = Album(musician_id=musician.id, name=name,
                         open_date=date, picture=db_image, genres=genres)
        return self.create(model=db_album)

    def update_album(self, album: Album, name: str,  date: datetime, genres: List[Genre], image: File, tracks_ids: List[int]):
        album.name = name
        album.open_date = date
        album.genres = genres
        if image:
            picture = album.picture
            album.picture = None
            if picture:
                file_cruds.delete_picture(file=picture)
            album.picture = self.create(image)
        tracks = album.tracks
        for index, track_id in enumerate(tracks_ids):
            for track in tracks:
                if track.id == track_id:
                    track.track_position = index

        self.db.add(album)
        self.db.commit()
        self.db.refresh(album)
        return album

    def get_musician_albums(self, musician_id: int) -> List[Album]:
        return self.db.query(Album).filter(Album.musician_id == musician_id).all()

    def get_musician_clips(self, musician_id: int):
        return self.db.query(Clip).filter(Clip.musician_id == musician_id).all()

    def create_clip(self, musician_id: int,  name: str, video_id: str, image_model: File):
        return self.create(Clip(musician_id=musician_id, picture=self.create(image_model), name=name, video_id=video_id,))

    def get_album(self, album_id: int) -> Album:
        return self.get(album_id, Album)

    def get_album_tracks(self, album_id: int) -> List[Track]:
        tracks = self.db.query(Track).filter(Track.album_id == album_id).all()
        return tracks if None in [track.track_position for track in tracks] else sorted(tracks, key=lambda track: track.track_position)

    def get_genres(self):
        return self.db.query(Genre).all()

    def create_genre(self, name: str, picture: File):
        return self.create(Genre(name=name, picture=self.create(picture)))

    def delete_track(self, track: Track):
        picture = track.picture
        if picture:
            track.picture = None
            file_cruds.delete_picture(file=picture)
        track_file = track.file
        path = '/'.join([settings.TRACKS_FOLDER, track_file.file_name])
        if Path(path).exists():
            os.remove(path)
        self.db.delete(track)
        self.db.commit()

    def get_track(self, track_id: int):
        return self.get(id=track_id, model=Track)

    def toggle_like_track(self, track_id: int, user_id: int):
        liked = self.get_liked_track_model(track_id=track_id, user_id=user_id)
        if not liked:
            self.create(FavoriteTracks(track_id=track_id, user_id=user_id))
            return True
        else:
            self.delete(model=liked)
            return False

    def toggle_like_musician(self, musician_id: int, user_id: int):
        liked = self.get_liked_musician_model(
            musician_id=musician_id, user_id=user_id)
        if not liked:
            self.create(FavoriteMusicians(
                musician_id=musician_id, user_id=user_id))
            return True
        else:
            self.delete(model=liked)
            return False

    def track_is_liked(self, track_id: int, user_id: int):
        return bool(self.get_liked_track_model(track_id=track_id, user_id=user_id))

    def musician_is_liked(self, musician_id: int, user_id: int):
        return bool(self.get_liked_musician_model(musician_id=musician_id, user_id=user_id))

    def get_liked_track_model(self, track_id: int, user_id: int) -> FavoriteTracks | None:
        return self.db.query(FavoriteTracks).filter(
            FavoriteTracks.track_id == track_id and FavoriteTracks.user_id == user_id).first()

    def get_liked_musician_model(self, musician_id: int, user_id: int) -> FavoriteMusicians | None:
        return self.db.query(FavoriteMusicians).filter(
            FavoriteMusicians.musician_id == musician_id and FavoriteMusicians.user_id == user_id).first()

    def delete_album(self, album: Album):
        for track in album.tracks:
            self.delete_track(track=track)
        picture = album.picture
        if picture:
            album.picture = None
            file_cruds.delete_picture(file=picture)
        self.db.delete(album)
        self.db.commit()

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
