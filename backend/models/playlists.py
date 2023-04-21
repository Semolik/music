import uuid
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from backend.db.base_class import Base
from backend.core.config import env_config
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from backend.models.tracks import Track


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
    description = Column(
        String(
            int(
                env_config.get('VITE_MAX_PLAYLIST_DESCRIPTION_LENGTH')
            )
        ),
        nullable=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    user = relationship(
        "User",
        foreign_keys=[user_id],
        backref=backref(
            "playlists",
            cascade="delete, delete-orphan"
        )
    )
    private = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    @hybrid_property
    def picture(self):
        tracks = self.playlists_tracks
        if tracks:
            return tracks.picture

    @hybrid_property
    def tracks_count(self):
        return len(self.playlists_tracks)

    @property
    def picture(self):
        tracks = self.playlists_tracks
        if tracks:
            return tracks[0].track.picture


class PlaylistTrack(Base):
    __tablename__ = 'playlists_tracks'
    playlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("playlists.id"),
        nullable=False,
        primary_key=True,
        index=True
    )
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        nullable=False,
        primary_key=True,
        index=True
    )
    track = relationship("Track", foreign_keys=[track_id], backref=backref(
        "playlists_tracks", cascade="delete, delete-orphan"))
    playlist = relationship("Playlist", foreign_keys=[playlist_id], backref=backref(
        "playlists_tracks", cascade="delete, delete-orphan"))

    @hybrid_property
    def is_available(self):
        return self.track.is_available


class FavoritePlaylist(Base):
    __tablename__ = 'favorites_playlists'
    playlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("playlists.id"),
        nullable=False,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
    )
