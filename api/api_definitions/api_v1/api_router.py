from fastapi import APIRouter
from .endpoints import api_endpoints
from .endpoints import penny_endpoints

api_router = APIRouter()
api_router.include_router(api_endpoints, prefix="/api/v1", tags=["api"])
api_router.include_router(penny_endpoints, prefix="/penny/v1", tags=["penny"])
