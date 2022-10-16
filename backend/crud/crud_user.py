from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from helpers.roles import set_status
from helpers.images import set_picture
from core.config import settings
from helpers.files import add_url
from crud.crud_file import FileCruds
from db.session import SessionLocal
from schemas.user import UserAuth, UserModifiable, UserRegister
from models.user import AnswerChangeRoleRequest, File, User, ChangeRoleRequest
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status


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

    def send_change_role_message(self, user_id, message, files_ids, account_status):
        db_change_role_request = ChangeRoleRequest(
            files_ids=files_ids,
            message=message,
            user_id=user_id,
            account_status=account_status
        )
        return self.create(db_change_role_request)

    def get_user_change_role_messages(self, user_id):
        records: List[ChangeRoleRequest] =\
            self.db.query(ChangeRoleRequest)\
            .order_by(ChangeRoleRequest.id.desc())\
            .filter(ChangeRoleRequest.user_id == user_id)\
            .all()
        return self.post_processing_change_role_messages(records)

    def get_all_change_role_messages(self, page: int = 1, page_size: int = 10):
        end = page * page_size
        records: List[ChangeRoleRequest] =\
            self.db.query(ChangeRoleRequest)\
            .order_by(ChangeRoleRequest.id.desc())\
            .slice(end-page_size, end)
        return self.post_processing_change_role_messages(records, add_user=True)

    def post_processing_change_role_messages(self, records: List[ChangeRoleRequest], add_user=False):
        result = list()
        for record in records:
            files = list()
            for file_id in record.files_ids:
                db_file = self.db.query(File).filter(
                    File.id == file_id).first()
                if db_file:
                    files.append(add_url(db_file))
            time_created: datetime = record.time_created
            time_created_str = time_created.strftime(settings.DATETIME_FORMAT)
            record_obj = jsonable_encoder(record)
            if add_user:
                user = record.user
                user_obj = jsonable_encoder(user)
                user_obj_with_pic = set_picture(user_obj, user.picture)
                record_obj['user'] = user_obj_with_pic
            record_obj['files'] = files
            record_obj['time_created'] = time_created_str
            result.append(record_obj)
        return result

    def is_has_change_role_messages(self, user_id):
        return bool(self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).first())

    def is_admin(self, user_id):
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception('Пользователь не найден')
        return db_user.is_superuser

    def get_change_role_message(self, request_id):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.id == request_id).first()

    def send_change_role_message_answer(self, request: ChangeRoleRequest, message: str, accept: bool, account_status: str = None):
        if request.answer:
            self.db.delete(request.answer)
            self.db.commit()
        db_answer = AnswerChangeRoleRequest(
            message=message,
            request_id=request.id,
            accept=accept
        )
        db_answer = self.create(db_answer)
        set_status_result = set_status(
            self.db, request.user, account_status if account_status else request.account_status)
        if not set_status_result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Попытка установить неподдерживаемый статус аккаунта")
        request.answer = db_answer
        answer_obj = jsonable_encoder(db_answer)
        answer_obj['time_created'] = db_answer.time_created.strftime(
            settings.DATETIME_FORMAT)
        return answer_obj


user_cruds = UserCruds()
