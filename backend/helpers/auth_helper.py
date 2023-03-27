from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from backend.core.config import settings


class Authenticate:
    def __init__(
        self,
        is_admin: bool = False,
        is_user: bool = False,
        default_user: bool = True,
        is_musician: bool = False,
        required: bool = True,
    ):
        self.types = []
        self.only_user = False
        self.required = required

        if is_admin:
            self.types.append(settings.UserTypeEnum.superuser)
        if is_user:
            self.types.append(settings.UserTypeEnum.user)
        if is_musician:
            self.types.append(settings.UserTypeEnum.musician)
        if len(self.types) == 0 and default_user:
            self.types.append(settings.UserTypeEnum.user)
        if self.types == [settings.UserTypeEnum.user]:
            self.only_user = True
        self.db = None
        self.current_user_id = None
        self.Authorize = None

    def __call__(self, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
        self.db = db
        self.current_user = None

        if self.required:
            Authorize.jwt_required()
            current_user_id = Authorize.get_jwt_subject()
        else:
            try:
                Authorize.jwt_optional()
                current_user_id = Authorize.get_jwt_subject()
            except:
                current_user_id = None

        if not current_user_id and not self.required:
            return self
        db_user = UserCruds(db).get_user_by_id(user_id=current_user_id)
        if not db_user:
            raise HTTPException(
                status_code=403,
                detail="Авторизованный пользователь не найден"
            )
        if not self.only_user and db_user.type not in self.types:
            raise HTTPException(
                status_code=403,
                detail=f"У вас недостаточно прав для выполнения этого действия, требуемый тип пользователя: {' '.join([settings.user_types_names.get(type) for type in self.types if type in settings.user_types_names])}",
            )
        self.current_user = db_user
        self.current_user_id = current_user_id
        return self
