import uuid

from app.db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    hashed_password = Column(String(), nullable=False)
    phone_number = Column(Integer(), nullable=True)
    is_superuser = Column(Boolean, default=False)
