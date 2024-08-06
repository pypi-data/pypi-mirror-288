import logging
import os
import sys
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
        record.label = f"[{os.environ.get('APP_NAME', 'genesis')}]"
        return super().format(record)

def setup_logger(name):
    logger = logging.getLogger(name)
    
    # Set log level from environment variable
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)
    
    if not logger.hasHandlers():
        log_handler = logging.StreamHandler(sys.stdout)
        formatter = CustomFormatter(
            fmt="%(timestamp)s %(label)s %(levelname)s: %(message)s"
        )
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

    return logger
