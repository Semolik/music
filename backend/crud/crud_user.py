from sqlalchemy.orm import Session
from schemas.user import UserModifiable, UserRegister
from models.user import Users
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()


def create_user(db: Session, user: UserRegister):
    password_hash = pwd_context.hash(user.password)
    db_user = Users(username=user.username, hashed_password=password_hash, first_name=user.first_name,
                    last_name=user.last_name)
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


def update_user(db: Session, user: Users, new_user_data: UserModifiable):
    print(new_user_data.dict())
    for var, value in new_user_data.dict().items():
        print(var, value)
        setattr(user, var, value) if value is not None else None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
