from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Table, Boolean
from sqlalchemy.orm import relationship
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID
import uuid


class FavoriteTracks(Base):
    __tablename__ = 'favorite_tracks'
    track_id = Column(UUID(as_uuid=True), ForeignKey(
        "tracks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    musician_id = Column(Integer, ForeignKey(
        "public_profiles.id"), nullable=False)
    musician = relationship("PublicProfile", foreign_keys=[musician_id])
    name = Column(
        String(int(env_config.get('VITE_MAX_ALBUM_NAME_LENGTH'))), nullable=False)
    open_date = Column(DateTime, nullable=False)
    picture_id = Column(UUID(as_uuid=True), ForeignKey("images.id"))
    picture = relationship("Image", foreign_keys=[picture_id])
    genres = relationship(
        "Genre", secondary=Table(
            "albums_genres_table",
            Base.metadata,
            Column("album_id", ForeignKey("albums.id"), primary_key=True),
            Column("genre_id", ForeignKey("genres.id"), primary_key=True),
        )
    )
    uploaded = Column(Boolean, nullable=False)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artist_id = Column(Integer, ForeignKey(
        "public_profiles.id"), nullable=False)
    artist = relationship("PublicProfile", foreign_keys=[artist_id])
    name = Column(
        String(int(env_config.get('VITE_MAX_TRACK_NAME_LENGTH'))), nullable=False)
    feat = Column(String(int(env_config.get('VITE_MAX_TRACK_FEAT_LENGTH'))))
    duration = Column(DECIMAL, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    album = relationship("Album", foreign_keys=[album_id], backref="tracks")
    track_position = Column(Integer)
    picture_id = Column(UUID(as_uuid=True), ForeignKey("images.id"))
    picture = relationship("Image", foreign_keys=[picture_id])


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(int(env_config.get('VITE_MAX_GENRE_NAME_LENGTH'))), nullable=False, unique=True)
    picture_id = Column(UUID(as_uuid=True), ForeignKey(
        "images.id"), nullable=False)
    picture = relationship("Image", foreign_keys=[picture_id])


class Clip(Base):
    __tablename__ = 'clips'

    id = Column(Integer, primary_key=True, index=True)
    musician_id = Column(
        Integer,
        ForeignKey("public_profiles.id"),
        nullable=False
    )
    musician = relationship(
        "PublicProfile",
        foreign_keys=[musician_id]
    )
    name = Column(
        String(int(env_config.get('VITE_MAX_CLIP_NAME_LENGTH'))),
        nullable=False
    )
    video_id = Column(
        String(int(env_config.get('VITE_MAX_YOUTUBE_VIDEOID_LENGTH'))),
        nullable=False
    )
    picture_id = Column(UUID(as_uuid=True), ForeignKey(
        "images.id"), nullable=False)
    picture = relationship("Image", foreign_keys=[picture_id])
