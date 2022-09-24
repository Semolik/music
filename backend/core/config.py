from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:4000']
    DATABASE_URI: Optional[str] = "sqlite:///example.db"
    FIRST_SUPERUSER: str = "admin"

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False


settings = Settings()
