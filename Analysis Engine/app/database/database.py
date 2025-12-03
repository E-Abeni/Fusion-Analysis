from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from app.configuration.connections_configuration import get_engine_database_connection_settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Base(DeclarativeBase):
    pass

def get_engine():
    settings = get_engine_database_connection_settings()
    if not settings:
        logging.error("Database connection settings are missing.")
        raise ValueError("Database connection settings are not configured properly.")
    if settings['engine_connection_string'] not in [None, '']:
        engine = create_engine(settings['engine_connection_string'])
        return engine
    else:
        engine = create_engine(f"postgresql+psycopg2://{settings['engine_username']}:{settings['engine_password']}@{settings['engine_host']}:{settings['engine_port']}/{settings['engine_database_name']}")
    return engine



def test_engine_connection(engine):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logging.info("[app.database] Database connection test successful.")
            return result.fetchone()[0] == 1
    except Exception as e:
        logging.error(f"[app.database] Database connection test failed: {e}")
        return False


if __name__ == "__main__":
    engine = get_engine()
    if test_engine_connection(engine):
        logging.info("[app.database] Engine is configured and connected successfully.")
    else:
        logging.error("[app.database] Failed to connect to the database with the provided engine.")