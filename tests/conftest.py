from starlette.testclient import TestClient
from backend.db.db import get_db
from backend.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from typing import Generator
from typing import Any
from backend.helpers.files import init_folders_structure
from backend.models.user import Base
from backend.api.api_v1.api import api_v1_router
from sqlalchemy_utils import database_exists, create_database
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from tests.utils.users import authentication_token_from_username
from tests.utils.names import generate_random_name


def start_application():
    app = FastAPI()
    app.include_router(api_v1_router)
    return app


@AuthJWT.load_config
def get_config():
    return settings.JWTsettings()


engine = create_engine(
    settings.TEST_DATABASE_URI
)
if not database_exists(engine.url):
    create_database(engine.url)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables.
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)
init_folders_structure()


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = start_application()
    yield _app
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    # transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    # transaction.rollback()
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


@pytest.fixture(scope="function")  # new function
def normal_user_token_cookies(client: TestClient, db_session):
    return authentication_token_from_username(
        client=client, username=settings.TEST_USER_USERNAME, db=db_session, password=settings.TEST_USER_PASSWORD
    )


@pytest.fixture(scope="function")  # new function
def normal_admin_token_cookies(client: TestClient, db_session):
    return authentication_token_from_username(
        client=client, username=settings.TEST_ADMIN_USERNAME, db=db_session, user_type=settings.UserTypeEnum.superuser
    )


@pytest.fixture(scope="function")  # new function
def normal_musician_token_cookies(client: TestClient, db_session):
    return authentication_token_from_username(
        client=client, username=settings.TEST_MUSICIAN_USERNAME, db=db_session, password=settings.TEST_MUSICIAN_PASSWORD, user_type=settings.UserTypeEnum.musician
    )


@pytest.fixture(scope="function")  # new function
def another_normal_musician_token_cookies(client: TestClient, db_session):
    return authentication_token_from_username(
        client=client, username=settings.TEST_ANOTHER_MUSICIAN_USERNAME, db=db_session, user_type=settings.UserTypeEnum.musician
    )


@pytest.fixture(scope="function")  # new function
def normal_user_2_token_cookies(client: TestClient, db_session):
    return authentication_token_from_username(
        client=client, username=settings.TEST_USER_USERNAME_2, db=db_session
    )


@pytest.fixture(scope="function")  # new function
def normal_user_3_token_cookies(client: TestClient, db_session):
    return authentication_token_from_username(
        client=client, username=settings.TEST_USER_USERNAME_3, db=db_session
    )


@pytest.fixture(scope="function")  # new function
def normal_users_tokens_cookies(client: TestClient, db_session):
    return [
        authentication_token_from_username(
            client=client, username=f'test_{generate_random_name(10)}', db=db_session, password=generate_random_name(10)
        )
        for _ in range(10)
    ]


@pytest.fixture(scope="function")  # new function
def normal_musicians_tokens_cookies(client: TestClient, db_session):
    return [
        authentication_token_from_username(
            client=client, username=f'test_{generate_random_name(10)}', db=db_session, password=generate_random_name(10), user_type=settings.UserTypeEnum.musician
        )
        for _ in range(10)
    ]
