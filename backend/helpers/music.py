from datetime import datetime
from typing import List
from backend.crud.crud_music import music_crud
from backend.helpers.images import set_picture
from backend.helpers.users import get_public_profile_as_dict
from backend.models.music import Album, Track
from backend.schemas.track import UploadTrackForm
from backend.crud.crud_user import user_cruds
from backend.db.base import crud_base
from pydub import AudioSegment
from fastapi import UploadFile, HTTPException, status
import uuid
import shutil
from backend.core.config import settings
from backend.models.user import File
import io


def save_track(upload_file: UploadFile, picture: File, user_id: int, track: UploadTrackForm):
    originalFileName = upload_file.filename
    uuid_filename = str(uuid.uuid4())
    buf = io.BytesIO()
    shutil.copyfileobj(upload_file.file, buf)
    buf.seek(0)
    fileName = uuid_filename + settings.SONGS_EXTENTION
    try:
        segment = AudioSegment.from_file(buf)
        segment.export('/'.join([settings.TRACKS_FOLDER, fileName]),
                       format=settings.SONGS_EXTENTION.replace('.', ''))
        db_file = crud_base.create(
            model=File(
                file_name=fileName,
                original_file_name=originalFileName,
                user_id=user_id,
                type='track'
            )
        )
        artist_public_profile = user_cruds.get_public_profile(user_id=user_id)
        db_picture = crud_base.create(picture) if picture else None
        db_track = crud_base.create(
            Track(
                artist_id=artist_public_profile.id,
                name=track.name,
                feat=track.feat,
                open_date=track.date,
                duration=round(segment.duration_seconds),
                file=db_file,
                album_id=track.album_id,
                picture=db_picture
            )
        )
        return db_track
    except:
        raise HTTPException(status_code=500, detail="поврежденный файл")


def set_album_info(db_album: Album, user_id: int | None = None, validate_date=False,):
    db_album_obj = db_album.as_dict()
    db_album_obj['year'] = db_album.open_date.year
    db_album_obj['date'] = db_album.open_date
    db_album_obj['musician'] = get_public_profile_as_dict(
        user_id=user_id, musician_id=db_album.musician_id)
    db_album_obj['genres'] = [set_picture(
        db_genre.as_dict(), db_genre.picture) for db_genre in db_album.genres]
    db_album_obj = set_picture(db_album_obj, db_album.picture)
    return db_album_obj


def set_album_tracks(db_album, db_album_obj):
    db_album_obj['tracks'] = [set_track_data(track)
                              for track in music_crud.get_album_tracks(album_id=db_album.id)]
    return db_album_obj


def set_track_data(track: Track):
    track_obj = set_picture(track.as_dict(), track.picture)
    track_obj['url'] = get_track_url(track)
    return track_obj


def set_full_track_data(track: Track):
    track_obj = set_track_data(track)
    track_obj['album'] = set_album_info(track.album)
    return track_obj


def get_track_url(track: Track):
    return ''.join(
        [settings.SERVER_LINK, settings.API_V1_STR, settings.UPLOADS_ROUTE, '/tracks/', track.file.file_name])


def validate_genres(genres_ids: List[int]):
    not_found_genres_ids = []
    genres = []
    if genres_ids:
        for genre_id in genres_ids:
            genre = music_crud.get_genre_by_id(id=genre_id)
            if not genre:
                not_found_genres_ids.append(genre_id)
            else:
                genres.append(genre)
        if len(not_found_genres_ids) > 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Жанры с id {','.join(map(str, not_found_genres_ids))} не найдены")
    return genres
