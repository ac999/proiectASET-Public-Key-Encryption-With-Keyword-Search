import logging
import functools

def create_logger():
    '''Creates a logging object and returns it'''

    logging.basicConfig(filename="logs/DEBUG.log",
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filemode= 'w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger

def log_exception(function):
    '''A decorator that wraps the passd in function and logs exceptions'''
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            err = "There was an exception in {}".format(function.__name__)
            logger.exception(err)
            raise

    return wrapper
