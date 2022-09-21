from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.api_v1.api import api_v1_router
app = FastAPI()


@AuthJWT.load_config
def get_config():
    return settings.JWTsettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# @app.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_refresh_token_required()

#     current_user = Authorize.get_jwt_subject()
#     new_access_token = Authorize.create_access_token(subject=current_user)

#     Authorize.set_access_cookies(new_access_token)
#     return {"msg": "The token has been refresh"}


# @app.delete('/logout')
# def logout(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()
#     Authorize.unset_jwt_cookies()
#     return {"msg": "Successfully logout"}


# @app.get('/me')
# def protected(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()

#     current_user = Authorize.get_jwt_subject()
#     return {"user": current_user}

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie"]
)
