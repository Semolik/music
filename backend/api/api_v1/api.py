from fastapi import APIRouter
from backend.api.api_v1.endpoints import auth,  user, roles, files, musician, statistics
from backend.api.api_v1.endpoints.music import albums, clips, genres, tracks


api_v1_router = APIRouter()

api_v1_router.include_router(auth.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(roles.router)
api_v1_router.include_router(files.router)
api_v1_router.include_router(musician.router)
api_v1_router.include_router(albums.router)
api_v1_router.include_router(clips.router)
api_v1_router.include_router(genres.router)
api_v1_router.include_router(tracks.router)
api_v1_router.include_router(statistics.router)
