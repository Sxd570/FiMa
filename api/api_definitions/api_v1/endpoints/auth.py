from fastapi import APIRouter
from shared.logger import Logger
from core.use_cases.auth import AuthUseCase
from core.models.io_models.auth_io_models import (
    LoginRequest,
    LoginPayload,
    SignupRequest,
    SignupPayload
)


logger = Logger(__name__)

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest):
    try:
        user_email = request.user_email
        password = request.password

        payload = LoginPayload(
            user_email=user_email,
            password=password
        )

        auth = AuthUseCase()

        response = auth.login(
            payload=payload
        )

        return response

    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise e    


@router.post("/signup")
async def signup(request: SignupRequest):
    try:
        user_email = request.user_email
        password = request.password
        username = request.username

        payload = SignupPayload(
            user_email=user_email,
            password=password,
            username=username
        )

        auth = AuthUseCase()

        response = auth.signup(
            payload=payload
        )

        return response
    except Exception as e:
        logger.error(f"Signup failed: {str(e)}")
        raise e