from fastapi import APIRouter
from .endpoints import api_endpoints

api_router = APIRouter()

api_router.include_router(api_endpoints, prefix="/api/v1", tags=["api"])
