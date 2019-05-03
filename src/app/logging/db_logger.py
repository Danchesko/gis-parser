import logging
import os

from config import logs_path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')

file_handler = logging.FileHandler(os.path.join(logs_path, 'db.log'))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
