from typing import List, Optional
from app.schemas.user import User

from pydantic import BaseModel
from uuid import UUID

# Shared properties
class TeamBase(BaseModel):
    name: str
    organisation: str
    num_member: int
    hardware_type: str
    software_type: str
    uuid_mentor: UUID


# Properties to receive via API on creation
class TeamCreate(TeamBase):
    pass


# Properties to receive via API on update
class TeamUpdate(TeamBase):
    pass


class TeamInDBBase(TeamBase):
    uuid: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Team(TeamInDBBase):
    uuid: UUID
    team_present: int = 0
    interview_comments: Optional[str] = None


# Additional properties stored in DB
class TeamInDB(TeamInDBBase):
    pass
