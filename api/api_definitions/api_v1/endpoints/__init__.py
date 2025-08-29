from fastapi import APIRouter
from . import auth
from . import budget
from . import goals
from . import transaction

api_endpoints = APIRouter()

api_endpoints.include_router(auth.router)
api_endpoints.include_router(budget.router)
api_endpoints.include_router(goals.router)
api_endpoints.include_router(transaction.router)