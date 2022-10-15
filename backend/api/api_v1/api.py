from fastapi import APIRouter
from .endpoints import auth, user, files, roles

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(files.router)
api_v1_router.include_router(roles.router)
