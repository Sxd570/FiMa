from fastapi import APIRouter
from . import chat

api_endpoints = APIRouter()

api_endpoints.include_router(chat.router)