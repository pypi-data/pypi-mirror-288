import os

import structlog
from samgis_core.utilities.session_logger import setup_logging


log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logging(log_level=log_level)
app_logger = structlog.stdlib.get_logger()
