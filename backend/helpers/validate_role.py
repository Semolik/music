from backend.crud.crud_user import UserCruds
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.core.config import settings


def validate_musician(db: Session, user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    if db_user.type != settings.UserTypeEnum.musician:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="необходим статус музыкант")
    return db_user


def validate_admin(db: Session, user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    if db_user.type != settings.UserTypeEnum.superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="необходим статус администратор")
    return db_user


def get_user(db: Session, user_id: int) -> User:
    db_user = UserCruds(db).get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    return db_user
