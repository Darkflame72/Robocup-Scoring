from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, teams, competitions

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(competitions.router, prefix="/competitions", tags=["competitions"])