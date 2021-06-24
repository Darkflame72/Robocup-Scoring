from typing import Any
from typing import List

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.models import team
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic.types import UUID4
from sqlalchemy.orm import Session

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


@router.get("/{team_uuid}", response_model=schemas.Team)
def read_team_by_uuid(
    user_uuid: UUID4,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific team by uuid.
    """
    team = crud.team.get(db, uuid=user_uuid)
    if team == current_user:
        return team
    if not crud.team.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return team


@router.put("/{team_uuid}", response_model=schemas.Team)
def update_team(
    *,
    db: Session = Depends(deps.get_db),
    user_uuid: UUID4,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a team.
    """
    team = crud.team.get(db, uuid=user_uuid)
    if not team:
        raise HTTPException(
            status_code=404,
            detail="The team with this uuid does not exist in the system",
        )
    team = crud.team.update(db, db_obj=team, obj_in=user_in)
    return team


@router.get("/members/{team_uuid}")
def get_team_members(
    *,
    db: Session = Depends(deps.get_db),
    team_uuid: UUID4,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    members = crud.team.get_team_members(db, uuid=team_uuid)
    return members
