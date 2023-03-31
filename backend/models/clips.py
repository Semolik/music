
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID


class Clip(Base):
    __tablename__ = 'clips'

    id = Column(Integer, primary_key=True, index=True)
    musician_id = Column(
        Integer,
        ForeignKey("public_profiles.id"),
        nullable=False
    )
    musician = relationship(
        "PublicProfile",
        foreign_keys=[musician_id],
        backref=backref("all_clips", cascade="all,delete")
    )
    name = Column(
        String(int(env_config.get('VITE_MAX_CLIP_NAME_LENGTH'))),
        nullable=False,
        index=True
    )
    video_id = Column(
        String(int(env_config.get('VITE_MAX_YOUTUBE_VIDEOID_LENGTH'))),
        nullable=False
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
