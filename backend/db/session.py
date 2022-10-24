from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from db.base_class import Base
from core.config import settings


engine = create_engine(  # 2
    settings.DATABASE_URI,
)

if not database_exists(engine.url):
    create_database(engine.url)

# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)  # 4
