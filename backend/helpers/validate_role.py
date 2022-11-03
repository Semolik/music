from backend.crud.crud_user import user_cruds
from fastapi import HTTPException, status


def validate_musician(user_id: int):
    db_user = get_user(user_id=user_id)
    if not db_user.is_musician:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="необходим статус музыкант")
    return db_user


def validate_admin(user_id: int):
    db_user = get_user(user_id=user_id)
    if not db_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="необходим статус администратор")
    return db_user


def get_user(user_id: int):
    db_user = user_cruds.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    return db_user
