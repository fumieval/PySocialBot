"""
PySocialBot utilities
"""
import time
import functools

def attempt(f, excepting=Exception, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except excepting:
        return None

def compose(f, g):
    return lambda *args: g(f(*args))

def retry(exception=Exception, interval=0, count=-1):
    """
    retry decorator.
    decorate function to retry.
    
    Keyword arguments:
    exception -- target exception.
    interval -- retry interval. (default is zero)
    count -- number of tries. (specify -1 to retry infinitely)
    """
    def wrapper(f):
        @functools.wraps(f)
        def _(*args, **kwargs):
            i = count
            while i != 0:
                try:
                    return f(*args, **kwargs)
                except exception:
                    time.sleep(interval)
                i -= 1
        return _
    return wrapper