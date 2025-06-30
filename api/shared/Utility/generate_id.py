import uuid

namespace_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')


def user_id(
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


def goal_id(
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