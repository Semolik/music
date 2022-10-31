from backend.initial_data import init
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api.api_v1.api import api_v1_router
from backend.initial_data import init
app = FastAPI()


@app.on_event("startup")
def startup():
    init()


@AuthJWT.load_config
def get_config():
    return settings.JWTsettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(api_v1_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Set-Cookie"]
)
