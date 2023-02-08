from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import backref
from sqlalchemy import event
from pathlib import Path
import os
from backend.core.config import settings


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
    artist = relationship(
        "PublicProfile",
        foreign_keys=[artist_id]
    )
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_TRACK_NAME_LENGTH')
            )
        ),
        nullable=False
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
            cascade="all,delete"
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
        cascade="all,delete"
    )

    @property
    def is_opened(self):
        return self.album.is_opened

    @property
    def album_uploaded(self):
        return self.album.uploaded

    @property
    def is_available(self):
        return self.is_opened and self.album_uploaded


@event.listens_for(Track, "after_delete")
def receive_after_delete(mapper, connection, target: Track):
    path = '/'.join([settings.TRACKS_FOLDER,
                     str(target.id)+settings.SONGS_EXTENTION])
    if Path(path).exists():
        os.remove(path)


class ListenTrackHistoryItem(Base):
    __tablename__ = 'listen_track_history'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        nullable=False
    )
    track = relationship(
        Track,
        foreign_keys=[track_id],
        backref=backref(
            "history",
            cascade="all,delete"
        )
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
            "listen_track_history",
            cascade="all,delete"
        )
    )
    listen_datetime = Column(
        DateTime(timezone=False),
        server_default=func.now()
    )
    listened = Column(
        Boolean,
        nullable=False,
        default=False
    )
