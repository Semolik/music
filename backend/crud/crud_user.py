from datetime import datetime
from typing import List
from backend.db.base import CRUDBase
from backend.helpers.roles import set_status
from backend.helpers.images import set_picture
from backend.core.config import settings
from backend.helpers.files import set_files_data
from backend.crud.crud_file import FileCruds
from backend.models.files import Image
from backend.models.music import Album
from backend.schemas.user import ChangeRoleRequestInfo, PublicProfileModifiable, UserAuth, UserModifiable, UserRegister
from backend.models.user import PublicProfile, User
from backend.models.roles import AnswerChangeRoleRequest, ChangeRoleRequest
from backend.models.user import PublicProfileLinks as PublicProfileLinksModel
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status


class UserCruds(CRUDBase):

    def __init__(self, session) -> None:
        self.db = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    def update(self, user: User, new_user_data: UserModifiable, userPic: Image) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        data_obj = new_user_data.dict()
        remove_picture = data_obj.pop('remove_picture')
        for var, value in data_obj.items():
            setattr(user, var, value) if value is not None else None
        if remove_picture:
            FileCruds(self.db).delete_image(user.picture)
        elif userPic:
            FileCruds(self.db).replace_old_picture(
                model=user, new_picture=userPic)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_public_profile(self, user_id):
        db_public_profile = self.db.query(PublicProfile).filter(
            PublicProfile.user_id == user_id).first()
        if db_public_profile:
            return db_public_profile
        db_user = self.get_user_by_id(user_id=user_id)
        links = PublicProfileLinksModel()
        new_db_public_profile = PublicProfile(
            name=' '.join(
                filter(None, [db_user.first_name, db_user.last_name])) or db_user.username,
            user_id=user_id,
            links=links
        )
        return self.create(new_db_public_profile)

    def get_public_profile_by_id(self, id):
        return self.db.query(PublicProfile).filter(
            PublicProfile.id == id).first()

    def update_public_profile(self, public_proile: PublicProfile, new_public_proile_data: PublicProfileModifiable,  userPublicPicture: Image) -> PublicProfile:
        if public_proile is None:
            raise Exception(
                'Update public_proile failed: public_proile is None')
        data_obj = new_public_proile_data.dict()
        remove_picture = data_obj.pop('remove_picture')
        for var, value in data_obj.items():
            if value is not None or var == 'description':
                setattr(public_proile, var, value)
        public_proile_links = public_proile.links
        public_proile_links_obj = public_proile_links.as_dict()
        public_proile_links_obj.pop('id')
        public_proile_links_obj.pop('public_profile_id')
        for var, _ in public_proile_links_obj.items():
            value = data_obj.get(var)
            setattr(public_proile_links, var, value)
        if remove_picture:
            FileCruds(self.db).delete_image(image=public_proile.picture)
        elif userPublicPicture:
            FileCruds(self.db).replace_old_picture(
                model=public_proile, new_picture=userPublicPicture)
        self.db.add(public_proile)
        self.db.commit()
        self.db.refresh(public_proile)
        return public_proile

    def send_change_role_message(self, user_id, message, files, account_status):
        db_change_role_request = ChangeRoleRequest(
            files=files,
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

    def get_all_change_role_messages(self, page: int = 1, filter: str = 'all', page_size: int = 10) -> List[ChangeRoleRequest]:
        end = page * page_size
        query = self.db.query(ChangeRoleRequest).order_by(
            ChangeRoleRequest.id.desc())
        if filter != 'all':
            query = query.where(ChangeRoleRequest.status == filter)
        return self.post_processing_change_role_messages(query.slice(end-page_size, end), add_user=True)

    def post_processing_change_role_messages(self, records: List[ChangeRoleRequest], add_user=False) -> ChangeRoleRequestInfo:
        result = list()
        for record in records:
            time_created: datetime = record.time_created
            time_created_str = time_created.strftime(settings.DATETIME_FORMAT)
            record_obj = jsonable_encoder(record)
            record_obj['answer'] = jsonable_encoder(record.answer)
            if add_user:
                user = record.user
                user_obj = jsonable_encoder(user)
                user_obj_with_pic = set_picture(user_obj, user.picture)
                record_obj['user'] = user_obj_with_pic
            record_obj['files'] = set_files_data(files=record.files)
            record_obj['time_created'] = time_created_str
            result.append(record_obj)
        return result

    def is_has_change_role_messages(self, user_id):
        return bool(self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).first())

    def is_user_have_active_change_role_messages(self, user_id: int, count: int) -> bool:
        result = self.db.query(ChangeRoleRequest)\
            .filter(ChangeRoleRequest.user_id == user_id, ChangeRoleRequest.status == 'in-progress')\
            .limit(count).all()
        return len(result) == count

    def is_admin(self, user_id):
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception('Пользователь не найден')
        return db_user.is_superuser

    def is_musician(self, user_id):
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception('Пользователь не найден')
        return db_user.is_musician

    def get_change_role_message(self, request_id):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.id == request_id).first()

    def send_change_role_message_answer(self, request: ChangeRoleRequest, message: str, request_status: settings.ALLOWED_STATUSES, account_status: str = None):
        if request.answer:
            self.db.delete(request.answer)
            self.db.commit()
        db_answer = AnswerChangeRoleRequest(
            message=message,
            request_id=request.id
        )
        db_answer = self.create(db_answer)
        set_status_result = True
        if account_status:
            set_status_result = set_status(
                self.db, request.user, account_status)
        elif request_status == 'successfully':
            set_status_result = set_status(
                self.db, request.user, request.account_status)
        if not set_status_result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Попытка установить неподдерживаемый статус аккаунта")
        request.answer = db_answer
        request.status = request_status
        self.db.commit()
        answer_obj = jsonable_encoder(db_answer)
        answer_obj['time_created'] = db_answer.time_created.strftime(
            settings.DATETIME_FORMAT)
        return answer_obj
