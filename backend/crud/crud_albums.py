from datetime import datetime
from typing import List
from backend.crud.crud_file import FileCruds
from backend.crud.crud_user import UserCruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.music import Album, Genre, Track, FavoriteAlbum
from backend.models.user import PublicProfile


class AlbumsCruds(CRUDBase):
    def get_album_tracks(self, album_id: int) -> List[Track]:
        tracks = self.db.query(Track).filter(Track.album_id == album_id).all()
        if None in [track.track_position for track in tracks]:
            return tracks
        return sorted(tracks, key=lambda track: track.track_position)

    def create_album(self, user_id: int, name: str,  date: datetime, picture: Image | None, genres: List[Genre]):
        db_image = self.create(model=picture) if picture else None
        musician = UserCruds(self.db).get_public_profile(user_id=user_id)
        db_album = Album(musician_id=musician.id, name=name,
                         open_date=date, picture=db_image, genres=genres, uploaded=False)
        return self.create(model=db_album)

    def update_album(self, album: Album, name: str,  date: datetime, genres: List[Genre], image: Image, tracks_ids: List[int]):
        album.name = name
        album.open_date = date
        album.genres = genres
        if image:
            FileCruds(self.db).replace_old_picture(
                model=album, new_picture=image)
        tracks = album.tracks
        for index, track_id in enumerate(tracks_ids):
            for track in tracks:
                if track.id == track_id:
                    track.track_position = index
        return self.create(model=album)

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

    def get_liked_albums(self, user_id: int) -> List[Album]:
        now = datetime.now()
        return self.db.query(Album).join(FavoriteAlbum).filter(Album.uploaded == True, FavoriteAlbum.user_id == user_id, Album.open_date <= now).all()
