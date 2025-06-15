from fastapi import APIRouter, HTTPException
from shared.logger import Logger
logger = Logger(__name__)

router = APIRouter()

@router.post("/login")
async def login():
    return {"message": "Login endpoint"}


@router.post("/signup")
async def signup():
    return {"message": "Signup endpoint"}