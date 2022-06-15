from functools import wraps

import structlog

log = structlog.get_logger()


def log_results(func):
    """
    Simple wrapper to log the results of a function call.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        rval = func(*args, **kwargs)
        log.msg('Generated Moves', name=str(getattr(func, '__qualname__', str(func))),
                args=args, kwargs=kwargs, return_val=rval)
        return rval
    return wrapper
