from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String,  ForeignKey, Table, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
import enum
from backend.core.config import settings


class ChangeRoleRequestStatus(str, enum.Enum):
    in_progress = 'in-progress'
    accepted = 'accepted'
    rejected = 'rejected'


class ChangeRoleRequest(Base):
    __tablename__ = 'change_role_requests'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    user = relationship(
        "User",
        foreign_keys=[user_id],
        backref=backref(
            "change_role_requests",
            cascade="delete, delete-orphan"
        )
    )
    message = Column(String)
    request_status = Column(
        Enum(ChangeRoleRequestStatus),
        nullable=False,
        default=ChangeRoleRequestStatus.in_progress,
    )
    time_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    files = relationship(
        "File", secondary=Table(
            "change_role_requests_files",
            Base.metadata,
            Column("change_role_request_id", ForeignKey(
                "change_role_requests.id"), primary_key=True),
            Column("file_id", ForeignKey("files.id"), primary_key=True),
        ), cascade="all,delete"
    )
    answer = relationship(
        "AnswerChangeRoleRequest",
        uselist=False,
        backref=backref(
            "request",
            cascade="all,delete",
            uselist=False
        )
    )


class AnswerChangeRoleRequest(Base):
    __tablename__ = 'answers_change_role_requests'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    time_created = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    message = Column(String)
    request_id = Column(Integer, ForeignKey(ChangeRoleRequest.id))
    accepted = Column(Boolean, default=False)
