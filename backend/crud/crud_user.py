from backend.db.base import CRUDBase
from backend.helpers.images import copy_image
from backend.crud.crud_file import FileCruds
from backend.models.files import Image
from backend.schemas.user import PublicProfileModifiable, UserAuth, UserModifiable, UserRegister
from backend.models.user import PublicProfile, User
from backend.models.user import PublicProfileLinks as PublicProfileLinksModel
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from backend.core.config import settings


class UserCruds(CRUDBase):

    def __init__(self, db) -> None:
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserRegister, user_type: settings.UserTypeEnum = settings.UserTypeEnum.user) -> User:
        password_hash = self.pwd_context.hash(user.password)
        user_in_data = jsonable_encoder(user)
        del user_in_data['password']
        db_user = User(
            hashed_password=password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            type=user_type
        )
        return self.create(db_user)

    def login(self, user: UserAuth) -> User | None:
        db_user = self.get_user_by_username(username=user.username)
        if not db_user:
            return None
        if not self.pwd_context.verify(user.password, db_user.hashed_password):
            return None
        return db_user

    def update_user(self, user: User, new_user_data: UserModifiable, userPic: Image) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        data_obj = new_user_data.dict()
        remove_picture = data_obj.pop('remove_picture')
        for var, value in data_obj.items():
            setattr(user, var, value) if value is not None else None
        if remove_picture and user.picture:
            self.delete(user.picture)
        elif userPic:
            FileCruds(self.db).replace_old_picture(
                model=user, new_picture=userPic)

        return self.create(user)

    def get_public_profile(self, user_id: int) -> PublicProfile:
        db_public_profile = self.db.query(PublicProfile).filter(
            PublicProfile.user_id == user_id).first()
        if db_public_profile:
            return db_public_profile
        db_user = self.get_user_by_id(user_id=user_id)
        links = PublicProfileLinksModel()
        name = ' '.join(
            filter(None, [db_user.first_name, db_user.last_name])) or db_user.username
        picture = copy_image(
            image=db_user.picture,
            db=self.db,
            user_id=user_id,
        )
        return self.create(PublicProfile(
            name=name,
            user_id=user_id,
            links=links,
            picture=picture
        ))

    def get_public_profile_by_id(self, id) -> PublicProfile:
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
            self.delete(public_proile.picture)
        elif userPublicPicture:
            FileCruds(self.db).replace_old_picture(
                model=public_proile, new_picture=userPublicPicture)

        return self.create(public_proile)

    def is_admin(self, user_id) -> bool:
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception('Пользователь не найден')
        return db_user.type == 'superuser'

    def is_musician(self, user_id) -> bool:
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise Exception('Пользователь не найден')
        return db_user.type == 'musician'

    def get_count(self) -> int:
        return self.db.query(User).count()

    def get_count_by_type(self, user_type) -> int:
        return self.db.query(User).filter(User.type == user_type).count()
