from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.models.user import User


def validate_authorized_user(Authorize: AuthJWT, db: Session) -> User:
    current_user_id = Authorize.get_jwt_subject()
    db_user = UserCruds(db).get_user_by_id(user_id=current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=403,
            detail="Авторизованный пользователь не найден"
        )
    return db_user
