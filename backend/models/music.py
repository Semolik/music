from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from backend.core.config import env_config


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    musician_id = Column(Integer, ForeignKey(
        "public_profiles.id"), nullable=False)
    musician = relationship("PublicProfile", foreign_keys=[musician_id])
    name = Column(
        String(int(env_config.get('VITE_MAX_ALBUM_NAME_LENGTH'))), nullable=False)
    open_date = Column(DateTime, nullable=False)
    picture_id = Column(Integer, ForeignKey("files.id", ondelete='SET NULL'))
    picture = relationship("File", foreign_keys=[picture_id])


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey(
        "public_profiles.id"), nullable=False)
    artist = relationship("PublicProfile", foreign_keys=[artist_id])
    name = Column(
        String(int(env_config.get('VITE_MAX_TRACK_NAME_LENGTH'))), nullable=False)
    feat = Column(String(int(env_config.get('VITE_MAX_TRACK_FEAT_LENGTH'))))
    open_date = Column(DateTime, nullable=False)
    duration = Column(DECIMAL, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    album = relationship("Album", foreign_keys=[album_id])
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    file = relationship("File", foreign_keys=[file_id])
    picture_id = Column(Integer, ForeignKey("files.id"))
    picture = relationship("File", foreign_keys=[picture_id])
