import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

# Shared properties
class CompetitionBase(BaseModel):
    name: str
    region: str
    date: datetime.date


# Properties to receive via API on creation
class CompetitionCreate(CompetitionBase):
    pass


# Properties to receive via API on update
class CompetitionUpdate(CompetitionBase):
    pass


class CompetitionInDBBase(CompetitionBase):
    uuid: Optional[UUID4] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Competition(CompetitionInDBBase):
    pass


# Additional properties stored in DB
class CompetitionInDB(CompetitionInDBBase):
    pass
