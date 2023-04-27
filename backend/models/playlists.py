import uuid
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from backend.db.base_class import Base
from backend.core.config import env_config
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref, object_session


class Playlist(Base):
    __tablename__ = 'playlists'

    def __init__(self, current_user_id=None, is_liked=False):
        self.current_user_id = current_user_id
        self.is_liked = is_liked

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

    @property
    def liked(self):
        is_liked = self.is_liked if hasattr(self, 'is_liked') else False
        if is_liked:
            return True
        current_user_id = self.current_user_id if hasattr(
            self, 'current_user_id') else None
        if current_user_id is None:
            return False
        return object_session(self).query(FavoritePlaylist).filter_by(
            playlist_id=self.id,
            user_id=current_user_id
        ).first() is not None


class ListenPlaylistHistoryItem(Base):
    __tablename__ = 'listen_playlist_history'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    playlist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("playlists.id", ondelete="CASCADE"),
        nullable=False
    )
    playlist = relationship(
        "Playlist",
        foreign_keys=[playlist_id],
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship(
        "User",
        foreign_keys=[user_id]
    )
    listen_datetime = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )


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
