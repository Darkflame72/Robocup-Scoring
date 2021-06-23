from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        out = cls.__name__[0]
        for i in range(1, len(cls.__name__)):
            if cls.__name__[i].isupper():
                out += "_"
            out += cls.__name__[i]
        return out.lower()
