import io
import random
import string
from fastapi.testclient import TestClient
from backend.crud.crud_genres import GenresCruds
from backend.helpers.images import save_image
from tests.utils.names import generate_random_name
baseGenreData = {
    "data": {

        "name": "test_genre_name",

    },
    "files": {
        "genrePicture": open("tests/test_files/test-profile-avatar.jpg", "rb"),
    }
}


def create_genre(client, db_session):
    admin_id = client.get("/users/me").json()["id"]
    genres_crud = GenresCruds(db_session)
    img = io.BytesIO(
        open("tests/test_files/test-profile-avatar.jpg", "rb").read()
    )
    img.name = "test-profile-avatar.jpg"
    img.seek(0)
    image = save_image(
        db=db_session,
        user_id=admin_id,
        upload_file=None,
        bytes_io_file=img
    )

    assert image is not None
    assert image.id is not None
    return genres_crud.create_genre(
        name=generate_random_name(10),
        picture=image
    )


def test_create_genre(client: TestClient, normal_admin_token_cookies):

    response = client.post(
        "/genres",
        data=baseGenreData.get("data"),
        cookies=normal_admin_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 200
    assert response.json()["name"] == baseGenreData.get("data")["name"]


def test_get_genre(client: TestClient):
    response = client.get(
        "/genres/1")
    assert response.status_code == 200


def test_get_genres(client: TestClient):
    response = client.get(
        "/genres")
    assert response.status_code == 200


def test_update_genre(client: TestClient, normal_admin_token_cookies, db_session):
    genre = create_genre(client, db_session)
    newGenreData = {
        "name": "test_genre_name_updated"
    }
    response = client.put(
        f"/genres/{genre.id}",
        data=newGenreData,
        cookies=normal_admin_token_cookies,
        files={
            "genrePicture": open("tests/test_files/test-profile-avatar.jpg", "rb"),
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == newGenreData["name"]


def test_delete_genre(client: TestClient, normal_admin_token_cookies, db_session):
    genre = create_genre(client, db_session)
    response = client.delete(
        f"/genres/{genre.id}",
        cookies=normal_admin_token_cookies
    )
    assert response.status_code == 204


def test_delete_genre_not_found(client: TestClient, normal_admin_token_cookies):
    response = client.delete(
        "/genres/10000",
        cookies=normal_admin_token_cookies
    )
    assert response.status_code == 404


def test_delete_genre_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.delete(
        "/genres/1",
        cookies=normal_user_token_cookies
    )
    assert response.status_code == 403


def test_update_genre_not_found(client: TestClient, normal_admin_token_cookies):
    response = client.put(
        "/genres/10000",
        data=baseGenreData.get("data"),
        cookies=normal_admin_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 404


def test_update_genre_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.put(
        "/genres/1",
        data=baseGenreData.get("data"),
        cookies=normal_user_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 403


def test_get_genre_not_found(client: TestClient):
    response = client.get(
        "/genres/10000")
    assert response.status_code == 404


def test_create_genre_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.post(
        "/genres",
        data=baseGenreData.get("data"),
        cookies=normal_user_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 403
