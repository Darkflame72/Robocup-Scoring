from typing import Any, Dict, Optional, Union
from uuid import uuid4
import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.competition import Competition
from app.schemas.competition import CompetitionCreate, CompetitionUpdate


class CRUDCompetition(CRUDBase[Competition, CompetitionCreate, CompetitionUpdate]):
    def get_by_date(self, db: Session, *, date: datetime.date) -> Optional[Competition]:
        return db.query(Competition).filter(Competition.date == date).first()

    def create(self, db: Session, *, obj_in: CompetitionCreate) -> Competition:
        db_obj = Competition(
            uuid=uuid4(),
            name=obj_in.name,
            region=obj_in.region,
            date=obj_in.date,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


competition = CRUDCompetition(Competition)
