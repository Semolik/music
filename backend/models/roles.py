from sqlalchemy.sql import func
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String,  ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import relationship


class ChangeRoleRequest(Base):
    __tablename__ = 'change_role_requests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", foreign_keys=[user_id])
    message = Column(String)
    files_ids = Column(ARRAY(Integer))
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
