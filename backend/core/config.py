from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_LINK: str = 'http://localhost:3000'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:4000', 'http://192.168.50.106:4000']
    # DATABASE_URI: Optional[str] = "sqlite:///example.db"
    DATABASE_URI: Optional[str] = "postgresql://postgres:aboba@localhost:5432/postgres"
    FIRST_SUPERUSER: str = "admin"
    IMAGES_FOLDER: str = 'assets/images'
    IMAGES_EXTENTION: str = '.png'
    UPLOADS_ROUTE: str = '/uploads'

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False


settings = Settings()
