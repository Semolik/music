from sqlalchemy.orm import Session
from crud.crud_file import FileCruds
from db.session import SessionLocal
from schemas.user import UserAuth, UserModifiable, UserRegister
from models.user import File, User
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder


class UserCruds:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db: Session = SessionLocal()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserRegister) -> User:
        password_hash = self.pwd_context.hash(user.password)
        user_in_data = jsonable_encoder(user)
        del user_in_data['password']
        db_user = User(hashed_password=password_hash, **user_in_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def login(self, user: UserAuth) -> User | None:
        db_user = self.get_user_by_username(username=user.username)
        if not db_user:
            return None
        if (not self.pwd_context.verify(user.password, db_user.hashed_password)):
            return None
        return db_user

    def update(self, user: User, new_user_data: UserModifiable, userPic: File) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        for var, value in new_user_data.dict().items():
            setattr(user, var, value) if value is not None else None
        if userPic:
            local_object_pic = self.db.merge(userPic)
            if user.picture:
                FileCruds(self.db).delete_file(user.picture)
            # user.picture = local_object_pic
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


user_cruds = UserCruds()
