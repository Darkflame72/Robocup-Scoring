from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[schemas.Team])
def read_teams(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    team = crud.team.get_multi(db, skip=skip, limit=limit)
    print(team[0].uuid_mentor)
    return team


@router.post("/", response_model=schemas.Team)
def create_team(
    *,
    db: Session = Depends(deps.get_db),
    team_in: schemas.TeamCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new team.
    """
    team = crud.team.create(db, obj_in=team_in)
    return team
