from copy import deepcopy
from shared.logger import Logger
from sqlalchemy import *
from domain.interfaces.auth_interface import AuthInterface
from domain.models.io_models.auth_io_models import *
from domain.models.tables.user import User
from shared.Utility.db_base import get_db_session

logger = Logger(__name__)

class AuthDatabase(AuthInterface):
    def __init__(self):
        self.db_session = None

    def create_user(self, db_payload: SignupDBRequest):
        try:
            user_id = db_payload.user_id
            user_email = db_payload.user_email
            username = db_payload.username
            password = db_payload.password

            filter_group = [
                User.user_id == user_id,
                User.user_email == user_email
            ]

            self.db_session = get_db_session()

            # Check if user already exists
            existing_user = self.db_session.query(
                User
            ).filter(
                *filter_group
            ).first()

            if existing_user:
                logger.error(f"User with ID {user_id} or email {user_email} already exists.")
                raise ValueError("User already exists")

            new_user = User(
                user_id=user_id,
                user_name=username,
                user_email=user_email,
                user_password=password
            )
            self.db_session.add(new_user)
            self.db_session.commit()

            return {
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            self.db_session.rollback()
            raise e
        
    def login(self, db_payload: LoginDBRequest):
        try:
            user_email = db_payload.user_email

            filter_group = [
                User.user_email == user_email,
            ]

            self.db_session = get_db_session()

            user = self.db_session.query(
                User
            ).filter(
                *filter_group
            ).first()

            if not user:
                logger.error(f"Login failed for email: {user_email}")
                raise ValueError("Invalid email or password")

            return LoginDBResponse(
                user_id=user.user_id,
                user_password=user.user_password
            )

        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            raise e