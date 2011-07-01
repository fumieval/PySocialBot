# coding:utf-8
"""
Data converting utility

>>> convert_encoding({u"spam": u"foobar", u"egg": [u"fizzbuzz", 1, 2]})
{'egg': ['fizzbuzz', 1, 2], 'spam': 'foobar'}

>>> convert_object({"spam": 42, "egg": "ham"})
{'egg': 'ham', 'spam': 42}

"""
import pysocialbot

try:
    strtype = unicode
except NameError:
    strtype = str

def convert_encoding(data, encode="utf-8"):
    """encode data encoding."""
    t = type(data)
    if t == int or t == str:
        return data
    elif t == strtype:
        return data.encode(encode)
    elif t == dict:
        return dict([(key.encode(encode), convert_encoding(data[key],encode)) for key in data])
    elif t == list:
        return [convert_encoding(item, encode) for item in data]

def convert_object(data):
    """convert dictionary to object."""
    if type(data) == dict:
        result = pysocialbot.Object()
        for key in data:
            result.__dict__[key] = convert_object(data[key])
        return result
    elif type(data) == list:
        return [convert_object(item) for item in data]  
    else:
        return data

def convert_class(data, T):
    """change object type."""
    result = T()
    result.__dict__ = data.__dict__
    return result

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()