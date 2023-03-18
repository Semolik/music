from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, scoped_session
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID
from backend.db.session import SessionLocal
from backend.models.albums import AlbumGenre
session = scoped_session(SessionLocal)


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_GENRE_NAME_LENGTH')
            )
        ),
        nullable=False,
        unique=True
    )
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id"),
        nullable=False
    )
    picture = relationship(
        "Image",
        foreign_keys=[picture_id],
        cascade="all,delete",
    )

    @property
    def likes(self):
        if not hasattr(self, '_likes_count'):
            self._likes_count = session.query(
                LovedGenre).filter_by(genre_id=self.id).count()
        return self._likes_count

    @property
    def album_count(self):
        if not hasattr(self, '_album_count'):
            self._album_count = session.query(
                AlbumGenre).filter_by(genre_id=self.id).count()
        return self._album_count


class LovedGenre(Base):
    __tablename__ = 'loved_genres'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    genre_id = Column(
        Integer,
        ForeignKey("genres.id"),
        nullable=False
    )
    genre = relationship(
        "Genre",
        foreign_keys=[genre_id],
        backref=backref(
            "loved_genres",
            uselist=True,
            cascade="delete, delete-orphan"
        )
    )
    user = relationship(
        "User",
        foreign_keys=[user_id],
        backref=backref(
            "loved_genres",
            uselist=True,
            cascade="delete, delete-orphan"
        )
    )
