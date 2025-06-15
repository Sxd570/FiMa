from fastapi import APIRouter
from . import auth

api_endpoints = APIRouter()

api_endpoints.include_router(auth.router)