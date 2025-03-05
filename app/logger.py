import os
from datetime import datetime
import logging
from pythonjsonlogger.json import JsonFormatter
from app.config import settings

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
log_file = os.path.join(LOG_DIR, f"app_{timestamp}.log")
error_log_file = os.path.join(LOG_DIR, f"error_{timestamp}.log")

logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL)

formatter = JsonFormatter()

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

error_file_handler = logging.FileHandler(error_log_file)
error_file_handler.setFormatter(formatter)
error_file_handler.setLevel(logging.ERROR)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_file_handler)
