from sqlalchemy.sql import func
from db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    username = Column(String, index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_musician = Column(Boolean, default=False)
    is_radio_station = Column(Boolean, default=False)
    files = relationship("File")
    picture = relationship("File", uselist=False, overlaps="files")


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    original_file_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="files",
                        foreign_keys=[user_id], overlaps="picture")
    type = Column(String, default='file')


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
    accept = Column(Boolean)
