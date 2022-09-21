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
        # Configure application to store and get JWT from cookies
        authjwt_token_location: set = {"cookies"}
        # Only allow JWT cookies to be sent over https
        authjwt_cookie_secure: bool = False
        # Enable csrf double submit protection. default is True
        authjwt_cookie_csrf_protect: bool = True
        # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
        # authjwt_cookie_samesite: str = 'lax'


settings = Settings()
