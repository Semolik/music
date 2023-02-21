import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from backend.db.base_class import Base
from backend.core.config import env_config
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref


class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_PLAYLIST_NAME_LENGTH')
            )
        ),
        nullable=False,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    private = Column(Boolean, nullable=False, default=True)


class PlaylistTrack(Base):
    __tablename__ = 'playlists_tracks'
    playlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        nullable=False
    )
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    track = relationship("Track", foreign_keys=[track_id], backref=backref(
        "playlists_tracks", cascade="delete, delete-orphan"))


class FavoritePlaylist(Base):
    __tablename__ = 'favorites_playlists'
    playlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("playlists.id"),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
