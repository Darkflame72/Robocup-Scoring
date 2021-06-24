from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base_class import Base


class User(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    hashed_password = Column(String(), nullable=False)
    phone_number = Column(Integer(), nullable=True)
    is_superuser = Column(Boolean, default=False)
