from services.aws.secret_manager import SecretManager
from shared.logger import Logger

logger = Logger(__name__)

FIMA_DB_SECRET = "fima-db-creds"

def get_db_path():
    return FIMA_DB_SECRET

def db_config():
    path = get_db_path()
    try:
        secret_manager_session = SecretManager()
        db_config = secret_manager_session.get_secret(path)
        return db_config
    except Exception as e:
        logger.error(f"Error retrieving database configuration: {e}")
        raise e
    

def get_db_config():
    return {
        "user": "fima",
        "password": "Fima1234!",
        "host": "localhost",
        "port": 3306,
        "database": "fima"
    }