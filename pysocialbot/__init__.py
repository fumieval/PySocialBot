"""
Python Bot Framework
"""
__author__ = "Fumiaki Kinoshita"
__credits__ = ["Fumiaki Kinoshita"]
__license__ = "BSD"
__version__ = "0.2.5"
__status__ = "Development"

class Object():
    
    """Generic Structure."""
    
    def __init__(self):
        pass
        
    def asdict(self):
        """Get data as dictionary."""
        result = {}
        for key in self.__dict__:
            if isinstance(self.__dict__[key], Object):
                result[key] = self.__dict__[key].asdict()
            else:
                result[key] = self.__dict__[key]
        return result
    
    def keys(self):
        """Get keys of objects."""
        return self.__dict__.keys()
    
    def __repr__(self):
        return self.asdict().__repr__()