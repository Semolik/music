from typing import List
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.models.user import User
from backend.core.config import settings


def validate_authorized_user(Authorize: AuthJWT, db: Session, types: List[settings.UserTypeEnum] = [settings.UserTypeEnum.user]) -> User:
    current_user_id = Authorize.get_jwt_subject()
    if not current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Необходима авторизация"
        )
    db_user = UserCruds(db).get_user_by_id(user_id=current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=403,
            detail="Авторизованный пользователь не найден"
        )
    if types != [settings.UserTypeEnum.user] and db_user.type not in types:
        raise HTTPException(
            status_code=403,
            detail=f"У вас недостаточно прав для выполнения этого действия, требуемый тип пользователя: {' '.join([settings.user_types_names.get(type) for type in types])}",
        )
    return db_user
