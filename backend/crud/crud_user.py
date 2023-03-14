from backend.db.base import CRUDBase
from backend.helpers.images import copy_image
from backend.crud.crud_file import FileCruds
from backend.models.files import Image
from backend.schemas.user import UserAuth,  UserRegister
from backend.models.user import PublicProfile, User
from backend.models.user import PublicProfileLinks
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

    def change_password(self, user: User, new_password: str) -> User:
        user.hashed_password = self.pwd_context.hash(new_password)
        return self.create(user)

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

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def check_password(self, user: User, password: str) -> bool:
        return self.pwd_context.verify(password, user.hashed_password)

    def update_user(self, user: User, first_name: str | None, last_name: str | None) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        user.first_name = first_name
        user.last_name = last_name
        return self.create(user)

    def update_user_avatar(self, user: User,  userPic: Image) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        if userPic and user.picture:
            FileCruds(self.db).replace_old_picture(
                model=user, new_picture=userPic)
        elif userPic:
            user.picture = userPic
        elif user.picture:
            self.delete(user.picture)

        return self.update(user)

    def get_public_profile(self, user_id: int) -> PublicProfile:
        db_public_profile = self.db.query(PublicProfile).filter(
            PublicProfile.user_id == user_id).first()
        if db_public_profile:
            return db_public_profile
        db_user = self.get_user_by_id(user_id=user_id)
        links = PublicProfileLinks()
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
            links=self.create(links),
            picture=picture
        ))

    def get_public_profile_by_id(self, id) -> PublicProfile:
        return self.db.query(PublicProfile).filter(
            PublicProfile.id == id).first()

    def update_public_profile(self, public_profile: PublicProfile, name: str, description: str, vk_username: str, telegram_username: str, youtube_channel_id: str) -> PublicProfile:
        if public_profile is None:
            raise Exception(
                'Update public_profile failed: public_profile is None')
        if name is not None:
            public_profile.name = name
        if description is not None:
            public_profile.description = description
        if vk_username is not None:
            public_profile.links.vk = vk_username
        if telegram_username is not None:
            public_profile.links.telegram = telegram_username
        if youtube_channel_id is not None:
            public_profile.links.youtube = youtube_channel_id
        self.update(public_profile.links)

        return self.update(public_profile)

    def update_public_profile_avatar(self, public_profile: PublicProfile,  userPublicPicture: Image) -> PublicProfile:
        if public_profile is None:
            raise Exception('Update user failed: user is None')
        if userPublicPicture and public_profile.picture:
            FileCruds(self.db).replace_old_picture(
                model=public_profile, new_picture=userPublicPicture)
        elif userPublicPicture:
            public_profile.picture = userPublicPicture
        elif public_profile.picture:
            self.delete(public_profile.picture)

        return self.update(public_profile)

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
