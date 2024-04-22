from models.user import *
from models.roles import *
from models.files import *
from models.genres import *
from models.albums import *
from models.tracks import *
from models.clips import *
from models.playlists import *
from models.slider import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from db.base_class import Base
from core.config import settings


engine = create_engine(
    settings.DATABASE_URI,
)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
