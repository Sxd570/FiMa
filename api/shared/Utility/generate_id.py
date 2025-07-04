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


def budget_id(
    user_id: str,
    category_id: str,
    allocated_month: str
) -> str:
    """
    Generate a unique budget identifier based on the user ID, category ID, and allocated month.

    Args:
        user_id (str): The unique identifier of the user.
        category_id (str): The unique identifier of the budget category.
        allocated_month (str): The month for which the budget is allocated.

    Returns:
        str: A unique identifier for the budget.
    """
    mapping = f"{user_id}_{category_id}_{allocated_month}"
    return str(uuid.uuid5(namespace_uuid, mapping))


def category_id(
    user_id: str,
    transaction_type_id: str,
    category_name: str
) -> str:
    """
    Generate a unique category identifier based on the user ID, transaction type ID, and category name.

    Args:
        user_id (str): The unique identifier of the user.
        transaction_type_id (str): The unique identifier of the transaction type.
        category_name (str): The name of the category.

    Returns:
        str: A unique identifier for the category.
    """
    sanitized_category_name = category_name.replace(" ", "").lower()
    mapping = f"{user_id}_{transaction_type_id}_{sanitized_category_name}"
    return str(uuid.uuid5(namespace_uuid, mapping))


def transaction_type_id(
    user_id: str,
    type_name: str
) -> str:
    """
    Generate a unique transaction type identifier based on the user ID and type name.

    Args:
        user_id (str): The unique identifier of the user.
        type_name (str): The name of the transaction type.

    Returns:
        str: A unique identifier for the transaction type.
    """
    sanitized_type_name = type_name.replace(" ", "").lower()
    mapping = f"{user_id}_{sanitized_type_name}"
    return str(uuid.uuid5(namespace_uuid, mapping))


def transaction_id(
    user_id: str,
    transaction_type_id: str,
    transaction_date: str,
    amount: float
) -> str:
    """
    Generate a unique transaction identifier based on the user ID, transaction type ID, date, and amount.

    Args:
        user_id (str): The unique identifier of the user.
        transaction_type_id (str): The unique identifier of the transaction type.
        transaction_date (str): The date of the transaction.
        amount (float): The amount of the transaction.

    Returns:
        str: A unique identifier for the transaction.
    """
    mapping = f"{user_id}_{transaction_type_id}_{transaction_date}_{amount}"
    return str(uuid.uuid5(namespace_uuid, mapping))