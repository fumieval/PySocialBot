"""
Common structures
"""

class Object(object):
    
    """Generic Structure."""
    
    def __init__(self, data={}):
        for key, value in data.iteritems():
            if isinstance(value, dict) and "Object" in value: 
                self.__dict__[key] = Object(value)
            else:
                self.__dict__[key] = value

    def realized(self):
        """Get data as a dictionary."""
        result = {"Object": True}
        for key in self.__dict__:
            if isinstance(self.__dict__[key], Object):
                result[key] = self.__dict__[key].realized()
            else:
                result[key] = self.__dict__[key]
        return result

    def iteritems(self):
        return self.__dict__.iteritems()
    
    def keys(self):
        """Get keys of object."""
        return self.__dict__.keys()
    
    def __repr__(self):
        return self.realized().__repr__()

class Lazy:
    def __init__(self, f):
        self.f = f
    def __call__(self, *args):
        return Lazy(self.f)
    def do(self):
        return self.f()

class Monad:
    """
    monad class.
    monads A B can be composed by A & B.
    Monad classes obey:
        Return(a) & f == f(a)
        m & Return == m
        (m & f) & g == m & lambda x: f(x) & g
    """
    def __and__(self, k):
        return Bind(self, k)
    
    def __rshift__(self, k):
        return self & (lambda _: k)
    
    def do(self):
        pass

class Bind(Monad):
    def __init__(self, x, k):
        self.x = x
        self.k = k
    def do(self):
        return self.k(self.x.do()).do()
    def __repr__(self):
        return "(%r & %r)" % (self.x, self.k)
    
class Action(Monad):
    def __init__(self, f):
        self.f = f
    def __call__(self):
        return Action(self.f)
    def do(self):
        return self.f()

class Return(Action):
    """
    This Action 
    """
    def __init__(self, x):
        self.x = x
        Action.__init__(self, lambda: x)
    def __repr__(self):
        return "Return(%r)" % self.x

class Composable:
    def __init__(self, f):
        self.f = f
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)
    def __pow__(self, other):
        return lambda *args, **kwargs: self.f(other(*args, **kwargs))
    def __repr__(self):
        return "Composable(%r)" % self.f