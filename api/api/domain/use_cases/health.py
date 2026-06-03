from shared.logger import Logger
from domain.database.health import Database

logger = Logger(__name__)


class HealthUseCase:
    def __init__(self):
        self.health_database = Database()

    def check(self) -> dict:
        try:
            result = self.health_database.ping()
            
            return {"status": "ok", **result}
        except Exception as e:
            logger.error(f"Error in check use case: {e}")
            raise e
