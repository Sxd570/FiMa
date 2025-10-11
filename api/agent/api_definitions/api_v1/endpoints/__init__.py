from fastapi import APIRouter
from . import chat
from . import agent

api_endpoints = APIRouter()

api_endpoints.include_router(chat.router)
api_endpoints.include_router(agent.router)