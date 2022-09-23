import logging
from core.security import get_password_hash
from schemas.user import UserRegister
from crud.crud_user import create_user, get_user_by_username
from db import base  # noqa: F401
from sqlalchemy.orm import Session
logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin"


def init_db(db: Session) -> None:  # 1
    if FIRST_SUPERUSER:
        user = get_user_by_username(db, username=FIRST_SUPERUSER)  # 2
        if not user:
            user_in = UserRegister(
                username=FIRST_SUPERUSER,
                first_name=FIRST_SUPERUSER,
                is_superuser=True,
                password='abobus'
            )
            user = create_user(db=db, user=user_in)
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )

