from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.core.config import env_config, settings
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref


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
    picture = relationship("Image", foreign_keys=[
                           picture_id], cascade="all,delete")
    # public_profile = relationship("PublicProfile", back_populates="user", uselist=False)


class PublicProfile(Base):
    __tablename__ = 'public_profiles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(
            int(
                env_config.get('VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH')
            )
        ),
        nullable=False
    )
    description = Column(
        String(
            int(
                env_config.get('VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH')
            )
        ),
        nullable=True
    )
    # links = relationship("PublicProfileLinks",
    #                      back_populates="public_profile", uselist=False)
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id", ondelete='SET NULL'))
    picture = relationship(
        "Image",
        foreign_keys=[picture_id],
        cascade="all,delete"
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
            cascade="all,delete"
        )
    )


class PublicProfileLinks(Base):
    __tablename__ = 'public_profiles_links'

    id = Column(Integer, primary_key=True, index=True)
    public_profile_id = Column(Integer, ForeignKey("public_profiles.id"))
    public_profile = relationship(
        "PublicProfile",
        backref=backref(
            "links",
            uselist=False,
            cascade="all,delete"
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
                env_config.get('VITE_MAX_YOUTUBE_ID_LENGTH')
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
