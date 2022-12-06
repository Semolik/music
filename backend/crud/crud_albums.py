from datetime import datetime
from typing import List
from backend.crud.crud_file import file_cruds
from backend.crud.crud_user import user_cruds
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.music import Album, Genre, Track
from backend.models.user import PublicProfile


class AlbumsCruds(CRUDBase):
    def get_album_tracks(self, album_id: int) -> List[Track]:
        tracks = self.db.query(Track).filter(Track.album_id == album_id).all()
        return tracks if None in [track.track_position for track in tracks] else sorted(tracks, key=lambda track: track.track_position)

    def create_album(self, user_id: int, name: str,  date: datetime, picture: Image | None, genres: List[Genre]):
        db_image = self.create(model=picture) if picture else None
        musician = user_cruds.get_public_profile(user_id=user_id)
        db_album = Album(musician_id=musician.id, name=name,
                         open_date=date, picture=db_image, genres=genres, uploaded=False)
        return self.create(model=db_album)

    def update_album(self, album: Album, name: str,  date: datetime, genres: List[Genre], image: Image, tracks_ids: List[int]):
        album.name = name
        album.open_date = date
        album.genres = genres
        if image:
            file_cruds.replace_old_picture(model=album, new_picture=image)
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

    def album_belongs_to_user(self, album: Album, user_id: int):
        db_public_profile: PublicProfile = self.db.query(PublicProfile).filter(
            PublicProfile.user_id == user_id).first()
        if not db_public_profile:
            return False
        return bool(album.musician_id == db_public_profile.id)

    def close_uploading(self, album: Album):
        album.uploaded = True
        self.db.add(album)
        self.db.commit()
        self.db.refresh(album)
        return album

    def delete_album(self, album: Album):
        for track in album.tracks:
            self.delete_track(track=track)
        picture = album.picture
        if picture:
            album.picture = None
            file_cruds.delete_image(image=picture)
        self.db.delete(album)
        self.db.commit()

    def get_album(self, album_id: int):
        return self.get(id=album_id, model=Album)


album_cruds = AlbumsCruds()
