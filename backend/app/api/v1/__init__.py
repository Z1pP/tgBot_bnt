from fastapi import APIRouter

from app.api.v1.routers.managers import router as managers_router
from app.api.v1.routers.reports import router as reports_router

base_router = APIRouter(prefix="/v1")
base_router.include_router(managers_router)
base_router.include_router(reports_router)
