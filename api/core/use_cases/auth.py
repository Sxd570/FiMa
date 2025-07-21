from infrastructure.aws.cognito import Cognito
from shared.logger import Logger
from shared.Utility.password_crypto import encrypt_password, decrypt_password
from shared.Utility.generate_id import (
    generate_user_id,
)
from core.database.auth import AuthDatabase
from core.models.io_models.auth_io_models import (
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
            password = payload.password

            encrypted_password = encrypt_password(password)

            db_payload = LoginDBRequest(
                user_email=user_email,
                password=encrypted_password
            )
            auth_database = AuthDatabase()
            
            db_response = auth_database.login(
                db_payload=db_payload
            )
            if not db_response:
                raise ValueError("Invalid email or password")
            
            decrypted_password = decrypt_password(db_response.user_password)

            if decrypted_password != password:
                raise ValueError("Invalid password")
            
            del db_response.user_password
            
            login_response = LoginResponse(
                user_id=db_response.user_id
            )
            
            return login_response
        except Exception as e:
            logger.error(f"Login usecase failed: {str(e)}")
            raise e
        

    def signup(self, payload: SignupPayload):
        try:
            username = payload.username
            user_email = payload.user_email
            password = payload.password

            user_id = generate_user_id(email=user_email)

            # Encrypt the password before saving to DB
            encrypted_password = encrypt_password(password)

            db_payload = SignupDBRequest(
                user_id=user_id,
                user_email=user_email,
                username=username,
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
