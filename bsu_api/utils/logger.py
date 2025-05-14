# Set up logging =====================================================
import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger(name: str = 'APILogger', level: int = logging.INFO) -> logging.Logger:
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # File handler
        file_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, 'info.log'),
            when='midnight',
            interval=1,
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

# Set up logging =====================================================