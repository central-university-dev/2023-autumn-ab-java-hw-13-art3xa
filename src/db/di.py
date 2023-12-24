
import psycopg2
from psycopg2 import OperationalError, ProgrammingError

from src.config.settings import get_settings

settings = get_settings()


def get_db():
    """Create and get database session.

    :yield: database session.
    """
    connection = None
    print(settings)
    try:
        connection = psycopg2.connect(
            database=settings.POSTGRES_DATABASE,
            user=settings.POSTGRES_USERNAME,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT)
        return connection
    except (OperationalError, ProgrammingError):
        connection.rollback()
        raise
