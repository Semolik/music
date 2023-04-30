import uuid
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship, backref, object_session
from backend.core.config import env_config, settings
from sqlalchemy.dialects.postgresql import UUID


class FavoriteMusicians(Base):
    __tablename__ = 'favorite_musicians'
    musician_id = Column(
        Integer,
        ForeignKey("public_profiles.id"),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    first_name = Column(
        String(
            int(
                env_config.get('VITE_MAX_FIRSTNAME_LENGTH')
            )
        ),
        nullable=True)
    last_name = Column(
        String(
            int(
                env_config.get('VITE_MAX_LASTNAME_LENGTH')
            )
        ),
        nullable=True)
    username = Column(
        String(
            int(
                env_config.get('VITE_MAX_LOGIN_LENGTH')
            )
        ),
        index=True,
        nullable=False
    )
    hashed_password = Column(
        String,
        index=True,
        nullable=False
    )
    type = Column(
        Enum(settings.UserTypeEnum),
        nullable=False,
        default=settings.UserTypeEnum.user
    )
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
            name='users_picture_id_fkey',
            ondelete='SET NULL'
        )
    )
    picture = relationship(
        "Image",
        foreign_keys=[picture_id],
        cascade="all,delete",
    )

    @property
    def is_admin(self):
        return self.type == settings.UserTypeEnum.superuser


class PublicProfile(Base):
    __tablename__ = 'public_profiles'

    def __init__(self, current_user_id=None, is_liked=False):
        self.current_user_id = current_user_id
        self.is_liked = is_liked

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH')
            )
        ),
        nullable=False,
        index=True
    )
    description = Column(
        String(
            int(
                env_config.get('VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH')
            )
        ),
        nullable=True
    )

    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id", ondelete='SET NULL'))
    picture = relationship(
        "Image",
        foreign_keys=[picture_id],
        cascade="all,delete",
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
            "public_profile",
            uselist=False,
            cascade="all,delete",
        )
    )

    @property
    def likes_count(self):
        if not hasattr(self, '_likes_count'):
            self._likes_count = object_session(self).query(
                FavoriteMusicians
            ).filter(
                FavoriteMusicians.musician_id == self.id
            ).count()
        return self._likes_count

    @property
    def liked(self):
        is_liked = self.is_liked if hasattr(self, 'is_liked') else False
        if is_liked:
            return True
        current_user_id = self.current_user_id if hasattr(
            self, 'current_user_id') else None
        if current_user_id is None:
            return False
        return object_session(self).query(
            FavoriteMusicians).filter(
                FavoriteMusicians.musician_id == self.id,
                FavoriteMusicians.user_id == self.current_user_id
        ).first() is not None


class PublicProfileLinks(Base):
    __tablename__ = 'public_profiles_links'

    id = Column(Integer, primary_key=True, index=True)
    public_profile_id = Column(Integer, ForeignKey("public_profiles.id"))
    public_profile = relationship(
        "PublicProfile",
        backref=backref(
            "links",
            uselist=False,
            cascade="delete, delete-orphan"
        )
    )
    telegram = Column(
        String(
            int(
                env_config.get('VITE_MAX_TELEGRAM_USERNAME_LENGTH')
            )
        )
    )
    youtube = Column(
        String(
            int(
                env_config.get('VITE_MAX_YOUTUBE_CHANNEL_ID_LENGTH')
            )
        )
    )
    vk = Column(
        String(
            int(
                env_config.get('VITE_MAX_VK_USERNAME_LENGTH')
            )
        )
    )


class ListenMusicianHistoryItem(Base):
    __tablename__ = 'listen_musician_history'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete='CASCADE'))
    user = relationship(
        "User",
        foreign_keys=[user_id],
    )
    musician_id = Column(Integer, ForeignKey(
        "public_profiles.id", ondelete='CASCADE'))
    musician = relationship(
        "PublicProfile",
        foreign_keys=[musician_id],
    )
    listen_datetime = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )
