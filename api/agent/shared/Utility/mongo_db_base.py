import os
from pymongo import MongoClient
from dotenv import load_dotenv
# from shared.logger import Logger

# logger = Logger(__name__)

load_dotenv()


class MongoDatabase:
    def __init__(self):
        self.config = {
            "user": os.environ["MONGO_USER"],
            "password": os.environ["MONGO_PASSWORD"],
            "host": os.environ["MONGO_HOST"],
            "port": os.environ["MONGO_PORT"],
            "database": os.environ["MONGO_DB_NAME"],
        }

        # Build Mongo URI
        uri = f"mongodb://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}?authSource=admin"

        try:
            # Create client
            self.client = MongoClient(uri)
            self.db = self.client[self.config["database"]]
            # logger.info("MongoDB connection established successfully")
        except Exception as e:
            # logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_db(self):
        """Return the MongoDB database object."""
        return self.db


# if __name__ == "__main__":
#     mongo_db = MongoDatabase()
#     db = mongo_db.get_db()

#     # Example usage: Fetch all documents from a collection
#     users = db["users"]
#     for user in users.find():
#         print(user)