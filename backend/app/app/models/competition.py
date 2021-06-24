import uuid

from app.db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


class Competition(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(20), nullable=False)
    region = Column(String(20), nullable=False)
    date = Column(Date(), nullable=False)
