import logging
from backend.schemas.user import UserRegister
from backend.crud.crud_user import UserCruds
from backend.db.session import SessionLocal
from backend.core.config import settings
logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin"


def init_db() -> None:  # 1
    logger.info("Инициализация базы данных")
    if FIRST_SUPERUSER:
        user_cruds = UserCruds(SessionLocal())
        user = user_cruds.get_user_by_username(FIRST_SUPERUSER)  # 2
        if not user:
            user_in = UserRegister(
                username=FIRST_SUPERUSER,
                first_name=FIRST_SUPERUSER,
                password='abobus123',
            )
            user_cruds.create_user(
                user_in, user_type=settings.UserTypeEnum.superuser)
            logger.info(f"Администратор {FIRST_SUPERUSER} создан")
        else:
            logger.warning(
                "Пропуск создания аккаунта администратора. Пользователь с юзернеймом "
                f"{FIRST_SUPERUSER} уже существует"
            )
    logger.info("Инициализация базы данных закончена")
