import logging
from pythonjsonlogger.json import JsonFormatter
import os
from datetime import datetime
from app.config import settings

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
log_file = os.path.join(log_dir, f"app_{timestamp}.log")

logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL)

formatter = JsonFormatter()

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
