from functools import lru_cache

from edgy import Registry

from .settings import database_settings


@lru_cache
def get_db_connection():
    return Registry(database=database_settings.database_url, echo=True)
