from sqlalchemy.orm import Session
from crud.crud_file import FileCruds
from db.session import SessionLocal
from schemas.user import UserAuth, UserModifiable, UserRegister
from models.user import File, User, ChangeRoleRequest
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder


class UserCruds:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db: Session = SessionLocal()

    def create(self, model):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

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
        if not self.pwd_context.verify(user.password, db_user.hashed_password):
            return None
        return db_user

    def update(self, user: User, new_user_data: UserModifiable, userPic: File) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        data_obj = new_user_data.dict()
        remove_picture = data_obj.pop('remove_picture')
        for var, value in data_obj.items():
            setattr(user, var, value) if value is not None else None
        if (userPic and user.picture) or remove_picture:
            FileCruds(self.db).delete_file(user.picture)
        if userPic:
            if user.picture:
                FileCruds(self.db).delete_file(user.picture)
            user.picture = self.create(userPic)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def send_change_role_message(self, user_id, message, files_ids):
        db_change_role_request = ChangeRoleRequest(files_ids=files_ids,
                                                   message=message, user_id=user_id)
        return self.create(db_change_role_request)

    def get_user_change_role_messages(self, user_id):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).all()


user_cruds = UserCruds()
