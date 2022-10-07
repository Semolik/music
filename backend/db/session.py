from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings


engine = create_engine(  # 2
    settings.DATABASE_URI,
    # required for sqlite
    # connect_args={"check_same_thread": False},  # 3
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)  # 4