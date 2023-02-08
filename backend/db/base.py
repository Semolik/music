from typing import Any, List


class CRUDBase:
    def __init__(self, db) -> None:
        self.db = db

    def get(self, id: Any, model):
        return self.db.query(model).filter(model.id == id).first()

    def get_multi(
            self, model, skip: int = 0, limit: int = 100, ) -> List:
        return self.db.query(model).offset(skip).limit(limit).all()  # 4

    def update(self, model):
        self.db.commit()
        self.db.refresh(model)
        return model

    def create(self,  model):
        self.db.add(model)
        self.update(model)
        return model

    def delete(self, model):
        self.db.delete(model)
        self.db.commit()
