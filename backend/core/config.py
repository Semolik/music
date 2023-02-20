from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Literal, Optional, Tuple, get_args
from dotenv import dotenv_values
import enum
env_config = {**dotenv_values('.env'), **dotenv_values(".env.local"), }


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_LINK: str = 'http://localhost:8000'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:4000', 'http://192.168.50.106:4000', 'http://192.168.1.133:4000']
    DATABASE_URI: Optional[str] = f"postgresql://{env_config['DB_USER']}:{env_config['DB_PASSWORD']}@{env_config['DB_HOST']}:{env_config['DB_PORT']}/{env_config['DB_NAME']}"
    TEST_DATABASE_URI: Optional[str] = DATABASE_URI + '_test'
    FIRST_SUPERUSER: str = "admin"
    ASSETS_FOLDER: str = 'assets/'
    IMAGES_FOLDER: str = ASSETS_FOLDER+'images'
    TRACKS_FOLDER: str = ASSETS_FOLDER+'tracks'
    OTHER_FILES_FOLDER: str = ASSETS_FOLDER+'other'
    IMAGES_EXTENTION: str = '.png'
    SONGS_EXTENTION: str = '.mp3'
    UPLOADS_ROUTE: str = '/uploads'
    OTHER_FILES_ROUTE: str = '/other/'
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M"
    ACTIVE_CHANGE_ROLE_REQUESTS_COUNT: int = 3
    SOCIAL_LINKS_FORMAT = {
        'telegram': 'https://t.me/{0}',
        'vk': 'https://vk.com/{0}',
        'youtube': 'https://www.youtube.com/channel/{0}',
        'youtube_video': 'https://www.youtube.com/watch?v={0}',
    }
    YOUTUBE_VIDEO = 'https://www.youtube.com/watch?v={0}'

    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user_password'
    TEST_USER_USERNAME_2 = 'test_user__2'
    TEST_USER_USERNAME_3 = 'test_user__3'
    TEST_USER_PASSWORD_3 = 'test_user_password_2'
    TEST_ADMIN_USERNAME = 'admin'
    TEST_MUSICIAN_USERNAME = 'musician_test'
    TEST_MUSICIAN_PASSWORD = 'musician_test_password'
    TEST_ANOTHER_MUSICIAN_USERNAME = 'musician_another'
    PAGINATION_LIMIT = 20
    # IMAGE_URL_BASE = ''.join(
    #     [SERVER_LINK, API_V1_STR, UPLOADS_ROUTE, '/images/', '{0}'])
    IMAGE_URL_BASE = ''.join(
        [API_V1_STR, UPLOADS_ROUTE, '/images/', '{0}'])
    UUID_REGEX = '[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}'

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False

    class UserTypeEnum(str, enum.Enum):
        musician = "musician"
        radiostaion = "radiostaion"
        user = "user"
        superuser = "superuser"
    user_types_names = {
        UserTypeEnum.superuser: "Администратор",
        UserTypeEnum.user: "Пользователь",
        UserTypeEnum.musician: "Музыкант",
    }

    AUTOCOMPLETE_SEARCH_ALBUM_LIMIT = int(
        env_config.get('VITE_AUTOCOMPLETE_SEARCH_ALBUM_LIMIT'))
    AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT = int(
        env_config.get('VITE_AUTOCOMPLETE_SEARCH_MUSICIAN_LIMIT'))
    AUTOCOMPLETE_SEARCH_TRACK_LIMIT = int(
        env_config.get('VITE_AUTOCOMPLETE_SEARCH_TRACK_LIMIT'))
    AUTOCOMPLETE_SEARCH_CLIP_LIMIT = int(
        env_config.get('VITE_AUTOCOMPLETE_SEARCH_CLIP_LIMIT'))
    AUTOCOMPLETE_SEARCH_ALL_LIMIT = 30

    SEARCH_ALBUM_LIMIT = int(env_config.get('VITE_SEARCH_ALBUM_LIMIT'))
    SEARCH_MUSICIAN_LIMIT = int(env_config.get('VITE_SEARCH_MUSICIAN_LIMIT'))
    SEARCH_TRACK_LIMIT = int(env_config.get('VITE_SEARCH_TRACK_LIMIT'))
    SEARCH_CLIP_LIMIT = int(env_config.get('VITE_SEARCH_CLIP_LIMIT'))

    USER_ACCOUNT_STATUSES_LIST = [
        user_type for user_type in UserTypeEnum.__members__.keys() if user_type != 'superuser']
    USER_ACCOUNT_STATUSES = Literal[tuple(USER_ACCOUNT_STATUSES_LIST)]


settings = Settings()
