from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.core.config import Settings


engine = create_engine(  # 2
    Settings.DATABASE_URI,
    # required for sqlite
    connect_args={"check_same_thread": False},  # 3
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)  # 4
