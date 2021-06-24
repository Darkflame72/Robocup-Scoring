from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Competition])
def read_competitions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    competition = crud.competition.get_multi(db, skip=skip, limit=limit)
    return competition


@router.post("/", response_model=schemas.Competition)
def create_competition(
    *,
    db: Session = Depends(deps.get_db),
    competition_in: schemas.CompetitionCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new competition.
    """
    competition = crud.competition.create(db, obj_in=competition_in)
    return competition


@router.get("/{competition_uuid}", response_model=schemas.Competition)
def read_competition_by_uuid(
    user_uuid: UUID4,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific competition by uuid.
    """
    competition = crud.competition.get(db, uuid=user_uuid)
    if competition == current_user:
        return competition
    if not crud.competition.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return competition


@router.put("/{competition_uuid}", response_model=schemas.Competition)
def update_competition(
    *,
    db: Session = Depends(deps.get_db),
    user_uuid: UUID4,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a competition.
    """
    competition = crud.competition.get(db, uuid=user_uuid)
    if not competition:
        raise HTTPException(
            status_code=404,
            detail="The competition with this uuid does not exist in the system",
        )
    competition = crud.competition.update(db, db_obj=competition, obj_in=user_in)
    return competition


@router.get("/members/{competition_uuid}")
def get_competition_members(
    *,
    db: Session = Depends(deps.get_db),
    competition_uuid: UUID4,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    members = crud.competition.get_competition_members(db, uuid=competition_uuid)
    return members
