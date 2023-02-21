from datetime import datetime
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,  Boolean
from sqlalchemy.orm import relationship
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
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
    album = relationship(
        "Album",
        foreign_keys=[album_id],
        backref=backref(
            "genres",
            cascade="all,delete"
        )
    )


class Album(Base):
    __tablename__ = 'albums'

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
        cascade="delete, delete-orphan",
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
