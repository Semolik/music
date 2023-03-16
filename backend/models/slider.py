import uuid
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from backend.db.base_class import Base
from backend.core.config import env_config
from sqlalchemy.orm import relationship


class Slide(Base):
    __tablename__ = 'slides'
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(
        String(
            int(env_config.get('MAX_SLIDE_NAME_LENGTH'))
        )
    )
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey('images.id')
    )
    picture = relationship(
        'Image',
        foreign_keys=[picture_id]
    )
    is_active = Column(
        Boolean,
        default=True
    )
    active_from = Column(
        DateTime,
        nullable=True
    )
    active_to = Column(
        DateTime,
        nullable=True
    )
    order = Column(
        Integer,
        nullable=True
    )
    url = Column(
        String,
        nullable=True
    )
