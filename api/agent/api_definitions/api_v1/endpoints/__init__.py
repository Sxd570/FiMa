from fastapi import APIRouter
from . import penny

api_endpoints = APIRouter()

api_endpoints.include_router(penny.router)