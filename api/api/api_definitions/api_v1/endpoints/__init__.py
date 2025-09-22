from fastapi import APIRouter
from . import auth
from . import budget
from . import goals
from . import transaction
from . import penny

api_endpoints = APIRouter()

api_endpoints.include_router(auth.router)
api_endpoints.include_router(budget.router)
api_endpoints.include_router(goals.router)
api_endpoints.include_router(transaction.router)


penny_endpoints = APIRouter()
penny_endpoints.include_router(penny.router)
