import time
from os import path
from pathlib import Path
import logging
from time import perf_counter
import datetime

log_date = datetime.datetime.now().strftime('%d-%B')
log_file_path = path.join(path.dirname(Path(__file__)), Path('logs'), f'middleware_{log_date}.log')

mware_logger = logging.getLogger('mware_logger')
mware_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(f'%(asctime)s - %(levelname)s:  %(message)s', '%d-%B-%y %H:%M:%S')

file_handler = logging.FileHandler(filename=log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

mware_logger.addHandler(file_handler)

mware_logger.info('---------------------------------------------------------------------------------------------------')


def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        mware_logger.info(f'{func.__name__}:{execution_time}')  # Response time is in seconds
        return result

    return wrapper
