
from sqlalchemy.orm import Session
import models, schemas
from auth import Auth

auth_handler = Auth()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    passwors_hash = auth_handler.encode_password(user.password)
    db_user = models.User(username=user.username, hashed_password=passwors_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(username, password, db):
    db_user = get_user_by_username(db, username=username)
    if not db_user:
        return 404
    if (not auth_handler.verify_password(password, db_user.hashed_password)):
        return 401
    return db_user
