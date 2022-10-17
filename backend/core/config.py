from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Literal, Optional, Tuple, get_args


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_LINK: str = 'http://localhost:3000'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:4000', 'http://192.168.50.106:4000']
    # DATABASE_URI: Optional[str] = "sqlite:///example.db"
    DATABASE_URI: Optional[str] = "postgresql://postgres:aboba@localhost:5432/postgres"
    TEST_DATABASE_URI: Optional[str] = "postgresql://postgres:aboba@localhost:5432/postgres_testt"
    FIRST_SUPERUSER: str = "admin"
    ASSETS_FOLDER: str = 'assets/'
    IMAGES_FOLDER: str = ASSETS_FOLDER+'images'
    OTHER_FILES_FOLDER: str = ASSETS_FOLDER+'other'
    IMAGES_EXTENTION: str = '.png'
    UPLOADS_ROUTE: str = '/uploads'
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M"
    ALLOWED_STATUSES = Literal['in-progress',
                               'successfully', 'rejected']
    ALLOWED_STATUSES_LIST: Tuple[str, ...] = get_args(ALLOWED_STATUSES)
    USER_ACCOUNT_STATUSES = Literal['is_radio_station',
                                    'is_musician', 'is_user']
    USER_ACCOUNT_STATUSES_LIST: Tuple[str, ...] = get_args(
        USER_ACCOUNT_STATUSES)

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False


settings = Settings()
