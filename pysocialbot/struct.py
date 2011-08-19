"""
Common struct
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
                result[key] = self.__dict__[key].asdict()
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
