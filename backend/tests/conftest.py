from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from typing import Generator
from typing import Any
from models.user import User, File
from models.user import Base
from db.db import get_db
from api.api_v1.api import api_v1_router
from sqlalchemy_utils import database_exists, create_database


def start_application():
    app = FastAPI()
    app.include_router(api_v1_router)
    return app

engine = create_engine(
    settings.TEST_DATABASE_URI #DATABASE_URI
)
if not database_exists(engine.url):
    create_database(engine.url)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(bind=engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
