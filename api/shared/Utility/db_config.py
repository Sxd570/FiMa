import os
from infrastructure.aws.secret_manager import SecretManager
from shared.logger import Logger

logger = Logger(__name__)
 
FIMA_RDS_SECRET = "fima-{}-rds-secret"
env = os.environ.get("ENVIRONMENT", "dev")

def get_db_path():
    return FIMA_RDS_SECRET.format(env)

def db_config():
    path = get_db_path()
    try:
        secret_manager_session = SecretManager()
        db_config = secret_manager_session.get_secret(path)
        return db_config
    except Exception as e:
        logger.error(f"Error retrieving database configuration: {e}")
        raise e
