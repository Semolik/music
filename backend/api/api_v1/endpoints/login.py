from fastapi import HTTPException, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from schemas.user import User
router = APIRouter()


@router.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != "test" or user.password != "test":
        raise HTTPException(
            status_code=401, detail="неправильное имя пользователя или пароль")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg": "Successfully login"}
