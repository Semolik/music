import logging
from schemas.user import UserRegister
from crud.crud_user import user_cruds
logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin"


def init_db() -> None:  # 1
    if FIRST_SUPERUSER:
        user = user_cruds.get_user_by_username(FIRST_SUPERUSER)  # 2
        if not user:
            user_in = UserRegister(
                username=FIRST_SUPERUSER,
                first_name=FIRST_SUPERUSER,
                is_superuser=True,
                password='abobus'
            )
            user = user_cruds.create_user(user_in)
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
