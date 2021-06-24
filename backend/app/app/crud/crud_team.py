from typing import Any, Dict, List, Optional, Union
from uuid import uuid4
from pydantic.types import UUID4

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.team import Team, TeamMember
from app.schemas.team import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def create(self, db: Session, *, obj_in: TeamCreate) -> Team:
        db_obj = Team(
            uuid=uuid4(),
            name=obj_in.name,
            organisation=obj_in.organisation,
            num_member=obj_in.num_member,
            uuid_mentor=obj_in.uuid_mentor,
            hardware_type=obj_in.hardware_type,
            software_type=obj_in.software_type,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_team_members(self, db: Session, uuid: UUID4) -> List[TeamMember]:
        return db.query(TeamMember).filter(TeamMember.uuid == uuid).all()


    # def update(
    #     self, db: Session, *, db_obj: Team, obj_in: Union[TeamUpdate, Dict[str, Any]]
    # ) -> Team:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if "password" in update_data:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def members(self, db:Session, team:UUID) -> Team:


team = CRUDTeam(Team)
