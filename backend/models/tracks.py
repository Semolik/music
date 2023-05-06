from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Boolean, event
from sqlalchemy.orm import relationship, backref, object_session
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from pathlib import Path
import os
from backend.core.config import settings
from sqlalchemy.ext.hybrid import hybrid_property
from backend.models.albums import Album
from backend.models.clips import Clip


class FavoriteTracks(Base):
    __tablename__ = 'favorite_tracks'
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )
    track = relationship(
        "Track",
        foreign_keys=[track_id],
        backref=backref(
            "favorite_tracks",
            cascade="all,delete"
        )
    )


class Track(Base):
    __tablename__ = 'tracks'

    def __init__(self, current_user_id=None, is_liked=False, **kwargs):
        self.current_user_id = current_user_id
        self.is_liked = is_liked
        super().__init__(**kwargs)

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    artist_id = Column(
        Integer,
        ForeignKey("public_profiles.id"),
        nullable=False
    )
    musician = relationship(
        "PublicProfile",
        foreign_keys=[artist_id]
    )
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_TRACK_NAME_LENGTH')
            )
        ),
        nullable=False,
        index=True
    )
    feat = Column(
        String(
            int(
                env_config.get('VITE_MAX_TRACK_FEAT_LENGTH')
            )
        )
    )
    duration = Column(
        DECIMAL,
        nullable=False
    )
    album_id = Column(
        Integer,
        ForeignKey("albums.id"),
        nullable=False
    )
    album = relationship(
        "Album",
        foreign_keys=[album_id],
        backref=backref(
            "tracks",
            cascade="delete, delete-orphan"
        )
    )
    track_position = Column(Integer)
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    picture = relationship(
        "Image",
        foreign_keys=[picture_id],
        cascade="all,delete",
    )

    @hybrid_property
    def is_opened(self):
        return self.album.is_opened

    @is_opened.expression
    def is_opened(cls):
        return Album.is_opened

    @hybrid_property
    def album_uploaded(self):
        return self.album.uploaded

    @album_uploaded.expression
    def album_uploaded(cls):
        return Album.uploaded

    @hybrid_property
    def is_available(self):
        return self.is_opened & self.album_uploaded

    @property
    def clip(self):
        return object_session(self).query(Clip).filter(Clip.track_id == self.id).first()

    @property
    def liked(self):
        is_liked = self.is_liked if hasattr(self, 'is_liked') else False
        if is_liked:
            return True
        current_user_id = self.current_user_id if hasattr(
            self, 'current_user_id') else None
        if current_user_id is None:
            return False
        return object_session(self).query(FavoriteTracks).filter_by(
            track_id=self.id,
            user_id=self.current_user_id).first() is not None


@event.listens_for(Track, "after_delete")
def receive_after_delete(mapper, connection, target: Track):
    path = '/'.join([settings.TRACKS_FOLDER,
                     str(target.id)+settings.SONGS_EXTENTION])
    if Path(path).exists():
        os.remove(path)


class ListenTrackHistoryItem(Base):
    __tablename__ = 'listen_track_history'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id", ondelete="CASCADE"),
        nullable=False
    )
    track = relationship(
        Track,
        foreign_keys=[track_id],
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship(
        "User",
        foreign_keys=[user_id],
    )
    listen_datetime = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )
    listened = Column(
        Boolean,
        nullable=False,
        default=False
    )
