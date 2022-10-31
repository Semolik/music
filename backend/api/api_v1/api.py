from fastapi import APIRouter
from backend.api.api_v1.endpoints import auth, user, files, roles, music

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(files.router)
api_v1_router.include_router(roles.router)
api_v1_router.include_router(music.router)
