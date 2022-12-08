# from db.repository.users import create_new_user
# from db.repository.users import get_user_by_email
from fastapi.testclient import TestClient
from backend.crud.crud_user import UserCruds
from sqlalchemy.orm import Session

from backend.schemas.user import UserRegister


def user_authentication_cookies(client: TestClient, username: str, password: str):
    user_data = UserRegister(username=username, password=password)
    response = client.post("/login", json=user_data.dict())
    return response.cookies


def authentication_token_from_username(client: TestClient, username: str, db: Session, admin=False):
    password = "random-passW0rd"
    user = UserCruds(db).get_user_by_username(username=username)
    if not user:
        user_data = UserRegister(
            username=username, password=password)
        user = UserCruds(db).create_user(user=user_data, admin=admin)
    return user_authentication_cookies(client=client, username=username, password=password)
