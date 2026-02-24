from fastapi import APIRouter
from shared.logger import Logger
from domain.use_cases.auth import AuthUseCase
from domain.models.io_models.auth_io_models import (
    LoginRequest,
    LoginPayload,
    SignupRequest,
    SignupPayload,
    LoginResponse,
    SignupResponse
)
from domain.exceptions import UserAlreadyExistsException, UserNotFoundException, InvalidCredentialsException


logger = Logger(__name__)

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
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

    except (UserNotFoundException, InvalidCredentialsException) as e:
        raise e
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise e    


@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest):
    try:
        user_email = request.user_email
        password = request.password
        user_name = request.user_name

        payload = SignupPayload(
            user_email=user_email,
            password=password,
            user_name=user_name
        )

        auth = AuthUseCase()

        response = auth.signup(
            payload=payload
        )

        return response
    except UserAlreadyExistsException as e:
        raise e
    except Exception as e:
        logger.error(f"Signup failed: {str(e)}")
        raise e