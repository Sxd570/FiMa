from services.aws.rds import RDS
from logger import Logger

logger = Logger()

def db_config():
    try:
        rds = RDS()
        db_config = rds.get_connection_config()
        return db_config
    except Exception as e:
        logger.error(f"Error retrieving database configuration: {e}")
        raise e
