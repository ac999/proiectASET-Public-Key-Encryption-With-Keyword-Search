from aspectlib import Aspect
import logger

@logger.log_exception
@Aspect
def log_errors(*args, **kwargs):
    try:
        yield
    except Exception as e:
        print("Raised %r for %s/%s" % (e, args, kwargs))
        raise
