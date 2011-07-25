"""
PySocialBot utilities
"""
import time
import functools
import itertools

def attempt(f, excepting=Exception, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except excepting:
        return None


def compose(f, g):
    return lambda *args: g(f(*args))

def ibranch(functions, *args, **kwargs):
    """
    >>> f = lambda x, y: x + y
    >>> g = lambda x, y: x * y
    >>> h = lambda x, y: x ** y
    >>> A = ibranch((f, g, h), 4, 3)
    >>> next(A)
    7
    >>> next(A)
    12
    >>> next(A)
    64
    """
    return itertools.imap(lambda f: f(*args, **kwargs), functions)

def merge(f, *functions):
    """
    >>> f = lambda x: x + 2
    >>> g = lambda x: x - 3
    >>> A = lambda x, y: x * y
    >>> F = merge(A, f, g) #λx.(x + 2)(x + 3)
    >>> F(2)
    -4
    >>> F(3)
    0
    >>> F(5)
    14
    """
    return lambda *args, **kwargs: f(*ibranch(functions, *args, **kwargs))

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

def convert_class(data, T):
    """change object class."""
    result = T()
    result.__dict__ = data.__dict__
    return result