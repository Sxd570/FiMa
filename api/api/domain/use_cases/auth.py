from fastapi import HTTPException
from shared.logger import Logger
from shared.Utility.password_crypto import encrypt_password, verify_password
from shared.Utility.generate_id import (
    generate_user_id,
)
from domain.database.auth import AuthDatabase
from domain.models.io_models.auth_io_models import (
    LoginPayload,
    LoginDBRequest,
    LoginResponse,
    SignupPayload,
    SignupDBRequest
)

logger = Logger(__name__)

class AuthUseCase:
    def login(self, payload: LoginPayload):
        try:
            user_email = payload.user_email
            input_password = payload.password

            # Prepare DB request without password (we only match on email/username)
            db_payload = LoginDBRequest(
                user_email=user_email
            )

            auth_database = AuthDatabase()
            db_response = auth_database.login(
                db_payload=db_payload
            )
            if not db_response:
                return LoginResponse(
                    user_id="",
                    status="user_not_found"
                )

            stored_hashed_password = db_response.user_password

            if not verify_password(stored_hashed_password, input_password):
                return LoginResponse(
                    user_id="",
                    status="wrong_password"
                )

            del db_response.user_password

            login_response = LoginResponse(
                user_id=db_response.user_id,
                status="success"
            )

            return login_response

        except Exception as e:
            logger.error(f"Login usecase failed: {str(e)}")
            raise e
        

    def signup(self, payload: SignupPayload):
        try:
            user_name = payload.user_name
            user_email = payload.user_email
            password = payload.password

            user_id = generate_user_id(email=user_email)

            # Encrypt the password before saving to DB
            encrypted_password = encrypt_password(password)

            db_payload = SignupDBRequest(
                user_id=user_id,
                user_email=user_email,
                user_name=user_name,
                password=encrypted_password
            )

            auth_database = AuthDatabase()
            db_response = auth_database.create_user(
                db_payload=db_payload
            )

            return db_response

        except Exception as e:
            logger.error(f"Signup usecase failed: {str(e)}")
            raise e
