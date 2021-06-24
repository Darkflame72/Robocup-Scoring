from typing import List
from typing import Optional

from app.schemas.user import User
from pydantic import BaseModel
from pydantic.types import UUID4

# Shared properties
class TeamBase(BaseModel):
    name: str
    organisation: str
    num_member: int
    hardware_type: str
    software_type: str
    uuid_mentor: UUID4


# Properties to receive via API on creation
class TeamCreate(TeamBase):
    pass


# Properties to receive via API on update
class TeamUpdate(TeamBase):
    pass


class TeamInDBBase(TeamBase):
    uuid: Optional[UUID4] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Team(TeamInDBBase):
    team_present: int = 0
    interview_comments: Optional[str] = None


# Additional properties stored in DB
class TeamInDB(TeamInDBBase):
    pass
