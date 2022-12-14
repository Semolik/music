from sqlalchemy.sql import func
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String,  ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship


class ChangeRoleRequest(Base):
    __tablename__ = 'change_role_requests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", foreign_keys=[user_id])
    message = Column(String)
    files = relationship(
        "File", secondary=Table(
            "change_role_requests_files",
            Base.metadata,
            Column("change_role_request_id", ForeignKey(
                "change_role_requests.id"), primary_key=True),
            Column("file_id", ForeignKey("files.id"), primary_key=True),
        )
    )
    status = Column(String, default='in-progress')
    account_status = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    answer = relationship("AnswerChangeRoleRequest", uselist=False)


class AnswerChangeRoleRequest(Base):
    __tablename__ = 'answers_change_role_requests'
    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String)
    request_id = Column(Integer, ForeignKey("change_role_requests.id"))
