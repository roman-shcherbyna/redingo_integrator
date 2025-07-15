import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
load_dotenv()

log_dir = os.path.abspath(os.getenv("LOGS_DIR"))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_dirs = {'info': os.path.join(log_dir, 'info'), 
            'debug': os.path.join(log_dir, 'debug'), 
            'errors': os.path.join(log_dir, 'errors')}

for path in log_dirs.values():
    if not os.path.exists(path):
        os.makedirs(path)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def create_timed_rotating_handler(log_path, level):
    today_date = datetime.now().strftime('%d_%m')
    log_filename = os.path.join(log_path, f'log_{today_date}.log')
    handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=30)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)


debug_handler = create_timed_rotating_handler(log_dirs['debug'], logging.DEBUG)
logger.addHandler(debug_handler)


info_handler = create_timed_rotating_handler(log_dirs['info'], logging.INFO)
logger.addHandler(info_handler)


error_handler = create_timed_rotating_handler(log_dirs['errors'], logging.ERROR)
logger.addHandler(error_handler)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Ctrl+C
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception