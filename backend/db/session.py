from backend.models.user import *
from backend.models.roles import *
from backend.models.files import *
from backend.models.genres import *
from backend.models.albums import *
from backend.models.tracks import *
from backend.models.clips import *
from backend.models.playlists import *
from backend.models.slider import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from backend.db.base_class import Base
from backend.core.config import settings


engine = create_engine(
    settings.DATABASE_URI,
)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
