from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Literal, Optional, Tuple, get_args
from dotenv import dotenv_values


env_config = {**dotenv_values('.env'), **dotenv_values(".env.local"), }


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_LINK: str = 'http://localhost:3000'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:4000', 'http://192.168.50.106:4000', 'http://192.168.1.133:4000']
    DATABASE_URI: Optional[str] = f"postgresql://{env_config['DB_USER']}:{env_config['DB_PASSWORD']}@{env_config['DB_HOST']}:{env_config['DB_PORT']}/{env_config['DB_NAME']}"
    TEST_DATABASE_URI: Optional[str] = DATABASE_URI+"_test"
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
    ALLOWED_STATUSES = Literal['in-progress',
                               'successfully', 'rejected']
    ALLOWED_STATUSES_FILTER = Literal[ALLOWED_STATUSES, 'all']
    ALLOWED_STATUSES_LIST: Tuple[str, ...] = get_args(ALLOWED_STATUSES)
    USER_ACCOUNT_STATUSES = Literal['radio_station',
                                    'musician', 'user']
    USER_ACCOUNT_STATUSES_LIST: Tuple[str, ...] = get_args(
        USER_ACCOUNT_STATUSES)
    ALL_USER_ACCOUNT_STATUSES = Literal[tuple(
        [*USER_ACCOUNT_STATUSES_LIST, 'superuser'])]
    ACTIVE_CHANGE_ROLE_REQUESTS_COUNT: int = 3
    SOCIAL_LINKS_FORMAT = {
        'telegram': 'https://t.me/{0}',
        'vk': 'https://vk.com/{0}',
        'youtube': 'https://www.youtube.com/channel/{0}'
    }
    YOUTUBE_VIDEO = 'https://www.youtube.com/watch?v={0}'

    TEST_USER_USERNAME = 'test_user'
    TEST_ADMIN_USERNAME = 'admin'

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False


settings = Settings()
