from fastapi import APIRouter

from app.routers.endpoints import login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

@api_router.get("/")
def ping():
    return "OK"