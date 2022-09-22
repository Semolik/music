import typing as t
from sqlalchemy.ext.declarative import as_declarative, declared_attr
class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}