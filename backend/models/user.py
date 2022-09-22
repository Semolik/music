from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean



class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    username = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String, index=True, nullable=False)