from typing import Any, List
from backend.db.session import session
from backend.db.base_class import Base


class CRUDBase:
    def __init__(self):
        self.db = session

    def get(self, id: Any, model):
        return self.db.query(model).filter(self.model.id == id).first()

    def get_multi(
        self,  *, skip: int = 0, limit: int = 100, model
    ) -> List:
        return self.db.query(model).offset(skip).limit(limit).all()  # 4

    def create(self,  *,  model):
        self.db.add(model)
        self.db.commit()  # 5
        self.db.refresh(model)
        return model
