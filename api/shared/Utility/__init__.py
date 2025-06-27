import os
import uuid

namespace_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')

def db_config_local():
    """
    Local mysql database configuration.
    This function returns the configuration for a local MySQL database connection for testing purposes.
    """
    user = os.environ.get("DB_USER", None)
    password = os.environ.get("DB_PASSWORD", None)
    host = os.environ.get("DB_HOST", None)
    database = os.environ.get("DB_DATABASE", None)
    port = os.environ.get("DB_PORT", None)

    if not user or not password or not host or not database or not port:
        raise ValueError("Database configuration is incomplete. Please set DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE, and DB_PORT environment variables.")

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