import os

def db_config_local():
    """
    Local mysql database configuration.
    This function returns the configuration for a local MySQL database connection for testing purposes.
    """
    user = os.environ.get("DB_USER", None)
    password = os.environ.get("DB_PASSWORD", None)
    host = os.environ.get("DB_HOST", None)
    database = os.environ.get("DB_DATABASE", None)

    if not user or not password or not host or not database:
        raise ValueError("Database configuration is incomplete. Please set DB_USER, DB_PASSWORD, DB_HOST, and DB_DATABASE environment variables.")
    
    return {
        "user": user,
        "password": password,
        "host": host,
        "database": database
    }