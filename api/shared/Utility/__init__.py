import os
import uuid
from dotenv import load_dotenv
load_dotenv()

namespace_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')

def db_config_local():
    """
    Local mysql database configuration.
    This function returns the configuration for a local MySQL database connection for testing purposes.
    """
    user = os.getenv("DB_USER", None)
    password = os.getenv("DB_PASSWORD", None)
    host = os.getenv("DB_HOST", None)
    database = os.getenv("DB_NAME", None)
    port = os.getenv("DB_PORT", None)

    if not user:
        raise ValueError("DB_USER environment variable is not set.")
    if not password:
        raise ValueError("DB_PASSWORD environment variable is not set.")
    if not host:
        raise ValueError("DB_HOST environment variable is not set.")
    if not database:
        raise ValueError("DB_NAME environment variable is not set.")
    if not port:
        raise ValueError("DB_PORT environment variable is not set.")
    
    
    return {
        "user": user,
        "password": password,
        "host": host,
        "database": database,
        "port": port
    }


def generate_user_id(
    email: str,
) -> str:
    """
    Generate a unique user ID based on the user's email and a UUID.

    Args:
        email (str): The email address of the user.

    Returns:
        str: A unique identifier for the user.
    """
    return str(uuid.uuid5(namespace_uuid, email))


def generate_goal_id(
    goal_name: str,
    user_id: str,
    ) -> str:
    """
    Generate a unique goal identifier based on the provided goal name and user ID.

    This function creates a deterministic UUID (version 5) by combining the user ID and goal name,
    ensuring that the same inputs always produce the same UUID.

    Args:
        goal_name (str): The name of the goal.
        user_id (str): The unique identifier of the user.

    Returns:
        str: A string representation of the generated UUID.
    """
    sanitized_goal_name = goal_name.replace(" ", "").lower()
    mapping = f"{user_id}_{sanitized_goal_name}"
    return str(uuid.uuid5(namespace_uuid, mapping))