from sqlalchemy.orm import DeclarativeBase
from app.database.database import get_engine, Base
from app.model import *
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    logging.info("Initializing database and creating tables...")
    engine = get_engine()
    Base.metadata.create_all(engine)
    logging.info("Database tables created successfully.")



