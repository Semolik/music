from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import SessionLocal

from db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):  # 1
    def __init__(self, model: Type[ModelType], db):  # 2
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    def get(self, id: Any) -> Optional[ModelType]:
        # 3
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,  *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()  # 4

    def create(self,  *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        self.db.commit()  # 5
        self.db.refresh(db_obj)
        return db_obj
