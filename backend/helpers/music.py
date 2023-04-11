
from typing import List
from uuid import UUID
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_genres import GenresCruds
from backend.crud.crud_albums import AlbumsCruds
from sqlalchemy.orm import Session
from backend.helpers.images import set_picture
from backend.helpers.urls import get_track_url_by_id
from backend.models.files import Image
from backend.models.playlists import Playlist
from backend.models.tracks import Track
from backend.schemas.music import UploadTrackForm
from backend.crud.crud_user import UserCruds
from backend.crud.crud_playlists import PlaylistsCrud
from backend.db.base import CRUDBase
from pydub import AudioSegment
from fastapi import UploadFile, HTTPException, status
import shutil
from backend.core.config import settings
import io
from datetime import datetime
from backend.schemas.music import Track as TrackSchema
from backend.models.albums import Album


def save_track(db: Session, album_id: int, upload_file: UploadFile, picture: Image, user_id: int, track: UploadTrackForm):
    buf = io.BytesIO()
    shutil.copyfileobj(upload_file.file, buf)
    buf.seek(0)
    try:
        segment = AudioSegment.from_file(buf)
        artist_public_profile = UserCruds(
            db).get_public_profile(user_id=user_id)
        db_picture = picture
        db_track = CRUDBase(db).create(
            Track(
                artist_id=artist_public_profile.id,
                name=track.name,
                feat=track.feat,
                duration=round(segment.duration_seconds),
                album_id=album_id,
                picture=db_picture,
            )
        )
        ext = settings.SONGS_EXTENTION
        segment.export('/'.join([settings.TRACKS_FOLDER, str(db_track.id)+ext]),
                       format=ext.replace('.', ''))
        return db_track
    except:
        raise HTTPException(status_code=422, detail="поврежденный файл")


def set_album_tracks(db: Session, db_album, db_album_obj, user_id: int = None):
    db_album_obj['tracks'] = [set_track_data(db=db, track=track, user_id=user_id)
                              for track in AlbumsCruds(db).get_album_tracks(album_id=db_album.id)]
    return db_album_obj


def set_tracks_likes(db: Session, tracks: List[Track], user_id: int):
    return [set_track_like(db=db, db_track=db_track, user_id=user_id) for db_track in tracks]


def set_track_like(db: Session, db_track: Track, user_id: int = None):
    track = TrackSchema.from_orm(db_track)
    track.liked = TracksCrud(db).track_is_liked(
        track_id=track.id, user_id=user_id) if user_id else False

    return track


def set_track_data(db: Session, track: Track, user_id: int = None):
    track_obj = set_picture(track.as_dict(), track.picture)
    track_obj['url'] = get_track_url(track=track)
    if user_id:
        track_obj['liked'] = TracksCrud(db).track_is_liked(
            track_id=track.id, user_id=user_id)
    return track_obj


def set_full_track_data(db: Session, track: Track, user_id: int = None):
    track_obj = set_track_data(track=track, db=db, user_id=user_id)
    track_obj['album'] = set_album_info(db_album=track.album)
    return track_obj


def get_track_url(track: Track):
    return get_track_url_by_id(track_id=track.id)


def validate_genres(db: Session, genres_ids: List[int]):
    not_found_genres_ids = []
    genres = []
    if genres_ids:
        for genre_id in genres_ids:
            genre = GenresCruds(db).get_genre_by_id(id=genre_id)
            if not genre:
                not_found_genres_ids.append(genre_id)
            else:
                genres.append(genre)
        not_fount_geres_count = len(not_found_genres_ids)
        if not_fount_geres_count > 0:
            letter = 'ы' if not_fount_geres_count > 1 else ''
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Жанр{letter} с id {','.join(map(str, not_found_genres_ids))} не найден{letter}")
    return genres


def is_album_showed(db: Session, album: Album, user_id: int):
    if not album.uploaded:
        return False
    if album.open_date > datetime.now() or not album.uploaded:
        if user_id is None or not AlbumsCruds(db).album_belongs_to_user(album=album, user_id=user_id):
            return False
    return True


def is_playlist_showed(playlist: Playlist, user_id: int):
    if playlist.private:
        if user_id is None or not playlist.user_id == user_id:
            return False
    return True


def validate_playlist_owner(db: Session, playlist_id: UUID, user_id: int) -> Playlist:
    playlist = PlaylistsCrud(db).get_playlist_info(playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    if not is_playlist_showed(playlist=playlist, user_id=user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    if playlist.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет доступа")
    return playlist


def validate_public_playlist(db: Session, playlist_id: UUID, user_id: int) -> Playlist:
    playlist = PlaylistsCrud(db).get_playlist_info(playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    if not is_playlist_showed(playlist=playlist, user_id=user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    return playlist


def validate_track(db: Session, track_id: UUID, user_id: int) -> Track:
    track = TracksCrud(db).get_track(track_id=track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Трек не найден")
    if not track.is_opened:
        if AlbumsCruds(db).album_belongs_to_user(album=track.album, user_id=user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Трек не опубликован")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Трек не найден")
    return track


def validate_tracks(db: Session, tracks_ids: List[UUID], user_id: int) -> List[Track]:
    not_found_tracks_ids = []
    tracks = []
    if tracks_ids:
        for track_id in tracks_ids:
            track = TracksCrud(db).get_track(track_id=track_id)
            if not track:
                not_found_tracks_ids.append(track_id)
            elif not track.is_opened:
                if AlbumsCruds(db).album_belongs_to_user(album=track.album, user_id=user_id):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Трек не опубликован")
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Трек не найден")
            else:
                tracks.append(track)
        not_fount_tracks_count = len(not_found_tracks_ids)
        if not_fount_tracks_count > 0:
            letter = 'ы' if not_fount_tracks_count > 1 else ''
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Трек{letter} с id {','.join(map(str, not_found_tracks_ids))} не найден{letter}")
    return tracks


def set_album_info(db_album: Album):
    db_album_obj = db_album.as_dict()
    db_album_obj['year'] = db_album.open_date.year
    db_album_obj['date'] = db_album.open_date

    db_album_obj['genres'] = [
        set_picture(
            db_genre.as_dict(),
            db_genre.picture
        )
        for db_genre in db_album.genres]
    db_album_obj = set_picture(db_album_obj, db_album.picture)
    return db_album_obj


def album_is_available(db: Session, user_id: int, album_id: int = None, album: Album = None, message: str = "Альбом не найден"):
    album_cruds = AlbumsCruds(db)
    if album_id is not None:
        album = album_cruds.get_album(album_id=album_id)
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    if not album.uploaded:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=message)
    if album.open_date > datetime.now() or not album.uploaded:
        if user_id is None or not album_cruds.album_belongs_to_user(album=album, user_id=user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=message)
    return album
