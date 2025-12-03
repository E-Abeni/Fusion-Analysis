import os
import logging
from app.configuration.initialize_configuration import initialize_configuration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

if not os.path.exists("kv_store.db"):
    logging.info("[app.Configuration] Configuration file not found. Initializing...")
    initialize_configuration()
else:
    logging.info("[app.Configuration] Configuration file found. Proceeding...")