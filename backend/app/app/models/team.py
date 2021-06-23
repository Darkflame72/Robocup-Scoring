from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.db.base_class import Base


class Team(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(60), nullable=False)
    organisation = Column(String(60), default="individual")
    num_member = Column(Integer, default=0)
    team_present = Column(Integer, default=0)
    interview_comments = Column(Text)
    uuid_mentor = Column(UUID(as_uuid=True), nullable=False)
    hardware_type = Column(String(64), nullable=False)
    software_type = Column(String(100), nullable=False)


class TeamMember(Base):
    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True,)
    uuid_team = Column(UUID(as_uuid=True), nullable=False)
    role = Column(String(length=10), nullable=True)
    # Column("competition", UUID(as_uuid=True), nullable=False),
