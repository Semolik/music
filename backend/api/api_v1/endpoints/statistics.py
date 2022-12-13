from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.crud.crud_change_roles import ChangeRolesCruds
from backend.helpers.validate_role import validate_admin
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.statistics import UsersStats
router = APIRouter(tags=['Статистика'], prefix='/statistics')


@router.get('', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UsersStats)
def get_users_count(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(db=db, user_id=current_user_id)
    user_count = UserCruds(db=db).get_count()
    admin_count = UserCruds(db=db).get_count_by_type('superuser')
    musician_count = UserCruds(db=db).get_count_by_type('musician')
    change_role_request_count = ChangeRolesCruds(
        db=db).get_not_answered_change_role_request_count()
    return UsersStats(
        user_count=user_count,
        admin_count=admin_count,
        change_role_request_count=change_role_request_count,
        musician_count=musician_count
    )
