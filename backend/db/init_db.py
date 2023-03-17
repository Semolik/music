import logging
from backend.schemas.user import UserRegister
from backend.crud.crud_user import UserCruds
from backend.db.session import SessionLocal
from backend.core.config import settings
logger = logging.getLogger(__name__)


def init_db() -> None:  # 1
    logger.info("Инициализация базы данных")
    user_cruds = UserCruds(SessionLocal())
    user = user_cruds.get_user_by_username(
        settings.DEFAULT_ADMIN_USERNAME)  # 2
    if not user:
        user_in = UserRegister(
            username=settings.DEFAULT_ADMIN_USERNAME,
            first_name=settings.DEFAULT_ADMIN_USERNAME,
            password='abobus123',
        )
        user_cruds.create_user(
            user_in, user_type=settings.UserTypeEnum.superuser)
        logger.info(f"Администратор {settings.DEFAULT_ADMIN_USERNAME} создан")
    else:
        logger.warning(
            "Пропуск создания аккаунта администратора. Пользователь с юзернеймом "
            f"{settings.DEFAULT_ADMIN_USERNAME} уже существует"
        )
    logger.info("Инициализация базы данных закончена")
