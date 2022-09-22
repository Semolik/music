from sqlalchemy.orm import Session
from backend.schemas.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: User):
    password_hash = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(username, password, db):
    db_user = get_user_by_username(db, username=username)
    if not db_user:
        return 404
    if (not pwd_context.verify(password, db_user.hashed_password)):
        return 401
    return db_user
