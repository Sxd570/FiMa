from infrastructure.aws.cognito import Cognito
from shared.logger import Logger
from shared.Utility.generate_id import (
    generate_user_id,
)
from core.database.auth import AuthDatabase
from core.models.io_models.auth_io_models import (
    LoginPayload,
    SignupPayload,
    SignupDBRequest
)

logger = Logger(__name__)

class AuthUseCase:
    def login(self, payload: LoginPayload):
        # Implement login logic here
        pass

    def signup(self, payload: SignupPayload):
        try:
            username = payload.username
            user_email = payload.user_email
            password = payload.password

            user_id = generate_user_id(email=user_email)

            db_payload = SignupDBRequest(
                user_id=user_id,
                user_email=user_email,
                username=username
            )

            auth_database = AuthDatabase()
            db_response = auth_database.create_user(
                db_payload=db_payload
            )

            return db_response

        except Exception as e:
            logger.error(f"Signup usecase failed: {str(e)}")
            raise e
