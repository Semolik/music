from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from pathlib import Path
import os
from backend.core.config import settings
from backend.models.user import User


class Image(Base):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(
        User.id), nullable=False)
    user = relationship("User", foreign_keys=[user_id])


@event.listens_for(Image, "after_delete")
def receive_after_delete(mapper, connection, target: Image):
    path = '/'.join([settings.IMAGES_FOLDER, str(target.id) +
                     settings.IMAGES_EXTENTION])
    if Path(path).exists():
        os.remove(path)


class File(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_file_name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship(User, foreign_keys=[user_id])


@event.listens_for(File, "after_delete")
def receive_after_delete(mapper, connection, target: File):
    path = os.path.join(settings.OTHER_FILES_FOLDER,
                        str(target.id)+target.extension)
    if Path(path).exists():
        os.remove(path)
