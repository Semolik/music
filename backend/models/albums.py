from datetime import datetime
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,  Boolean, func
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, object_session, relationship
from sqlalchemy.ext.hybrid import hybrid_property


class AlbumGenre(Base):
    __tablename__ = 'album_genres'

    album_id = Column(
        Integer,
        ForeignKey("albums.id"),
        primary_key=True
    )
    genre_id = Column(
        Integer,
        ForeignKey("genres.id"),
        primary_key=True
    )


class Album(Base):
    __tablename__ = 'albums'

    def __init__(self, current_user_id=None, is_liked=False):
        self.current_user_id = current_user_id
        self.is_liked = is_liked
    id = Column(Integer, primary_key=True, index=True)
    musician_id = Column(
        Integer,
        ForeignKey("public_profiles.id"),
        nullable=False
    )
    musician = relationship(
        "PublicProfile",
        foreign_keys=[musician_id],
        backref=backref("albums", cascade="all,delete")
    )
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id")
    )
    picture = relationship(
        "Image",
        foreign_keys=[picture_id],
        cascade="all,delete",
        backref="album_picture"
    )
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_ALBUM_NAME_LENGTH')
            )
        ),
        nullable=False,
        index=True
    )
    open_date = Column(
        DateTime,
        nullable=False
    )
    uploaded = Column(
        Boolean,
        nullable=False,
        default=False
    )
    genres = relationship(
        "Genre",
        secondary="album_genres",
        backref="albums"
    )

    @hybrid_property
    def is_opened(self):
        return self.open_date <= datetime.now()

    @is_opened.expression
    def is_opened(cls):
        return cls.open_date <= datetime.now()

    @hybrid_property
    def year(self):
        return self.open_date.year

    @hybrid_property
    def is_available(self):
        return self.is_opened & self.uploaded

    @hybrid_property
    def musician_user_id(self):
        return self.musician.user_id

    @property
    def likes_count(self):
        return object_session(self).query(FavoriteAlbum).filter(FavoriteAlbum.album_id == self.id).count()

    @property
    def liked(self):
        is_liked = self.is_liked if hasattr(self, 'is_liked') else False
        if is_liked:
            return True
        current_user_id = self.current_user_id if hasattr(
            self, 'current_user_id') else None
        if current_user_id is None:
            return False
        return object_session(self).query(FavoriteAlbum).filter(FavoriteAlbum.album_id == self.id, FavoriteAlbum.user_id == self.current_user_id).first() is not None


class ListenAlbumHistoryItem(Base):
    __tablename__ = 'listen_album_history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    album_id = Column(
        Integer,
        ForeignKey("albums.id", ondelete="CASCADE"),
        primary_key=True
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],

    )
    album = relationship(
        "Album",
        foreign_keys=[album_id],
    )

    listen_datetime = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )


class FavoriteAlbum(Base):
    __tablename__ = 'favorite_albums'
    album_id = Column(
        Integer,
        ForeignKey(Album.id),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )
    album = relationship(
        Album,
        foreign_keys=[album_id],
        backref=backref(
            "favorite_albums",
            cascade="all,delete"
        )
    )
    user = relationship(
        "User",
        foreign_keys=[user_id],
        backref=backref(
            "favorite_albums",
            cascade="all,delete"
        )
    )
