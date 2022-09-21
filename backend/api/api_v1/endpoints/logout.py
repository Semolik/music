from fastapi import Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
router = APIRouter()


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
