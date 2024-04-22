import logging
from schemas.user import UserRegister
from crud.crud_user import UserCruds
from db.session import SessionLocal
from core.config import settings
from fastapi.logger import logger
from passlib import pwd

def init_db() -> None:  # 1
    logger.info("Инициализация базы данных")
    user_cruds = UserCruds(SessionLocal())
    user = user_cruds.get_user_by_username(
        settings.DEFAULT_ADMIN_USERNAME)  # 2
    if not user:
        password = pwd.genword(length=12, charset="ascii_72")
        user_in = UserRegister(
            username=settings.DEFAULT_ADMIN_USERNAME,
            first_name=settings.DEFAULT_ADMIN_USERNAME,
            password=password
        )
        user_cruds.create_user(
            user_in, user_type=settings.UserTypeEnum.superuser)
        logger.warning("Superuser created successfully")
        logger.warning(f"Superuser username: {settings.DEFAULT_ADMIN_USERNAME}")
        logger.warning(f"Superuser password: {password}")
    else:
        logger.warning(
            "Пропуск создания аккаунта администратора. Пользователь с юзернеймом "
            f"{settings.DEFAULT_ADMIN_USERNAME} уже существует"
        )
    logger.info("Инициализация базы данных закончена")
