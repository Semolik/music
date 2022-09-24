from fastapi import Depends, APIRouter, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from db.db import get_db
from schemas.user import UserRegister
from models.user import Users as users_model
from crud.crud_user import create_user
from typing import Any
router = APIRouter()


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}
