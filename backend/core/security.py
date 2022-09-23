from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from typing import Optional, MutableMapping, List, Union

from backend.schemas.user import UserInfo

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[UserInfo]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # 1
        return None
    return user
