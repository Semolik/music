import uuid
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from backend.db.base_class import Base
from backend.core.config import env_config
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class SupportMessageStatus(enum.Enum):
    PENDING = 'pending'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'


class SupportMessageType(enum.Enum):
    PASSWORD_RECOVERY = 'password_recovery'
    SUPPORT = 'support'


class SupportMessage(Base):
    __tablename__ = 'support_messages'

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
    email = Column(
        String(
            int(env_config.get('MAX_EMAIL_LENGTH'))
        ),
        nullable=False
    )
    message = Column(
        String(
            int(env_config.get('MAX_SUPPORT_MESSAGE_LENGTH'))
        ),
        nullable=False
    )
    status = Column(
        Enum(SupportMessageStatus),
        default=SupportMessageStatus.PENDING
    )
    type = Column(
        Enum(SupportMessageType),
        default=SupportMessageType.SUPPORT
    )
    created_at = Column(DateTime, server_default=func.now())

    @property
    def login(self):
        return self.user.username
