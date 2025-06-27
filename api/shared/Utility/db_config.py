import os
from . import db_config_local
from services.aws.rds import get_db_config

config_level = os.environ.get("CONFIG_LEVEL", "local")


def db_config_cloud():
    return get_db_config()
    

def db_config():
    if config_level == "local":
        return db_config_local()
    else:
        return db_config_cloud()