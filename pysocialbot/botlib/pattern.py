import re

class Pattern():
    """Trigger class."""
    def __init__(self):
        pass
    def __call__(self, text, env=None):
        """Always returns true."""
        return True
    def __and__(self, other):
        return PatternAnd(self, other)
    def __xor__(self, other):
        return PatternXor(self, other)
    def __or__(self, other):
        return PatternOr(self, other)
    def __invert__(self):
        return PatternInvert(self)
    def __repr__(self):
        return "Trigger()"
    def check(self, env):
        """synonymous with __call__."""
        return self(env)
    def invert(self):
        """synonymous with __invert__."""
        return self.__invert__()

class PatternAnd(Pattern):
    """Intersection between triggers."""
    def __init__(self, left, right):
        Pattern.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, text, env=None):
        return self.left(text, env) and self.right(text, env)
    def __repr__(self):
        return "%s & %s" % (repr(self.left), repr(self.right))

class PatternXor(Pattern):
    """Exclusive intersection between triggers."""
    def __init__(self, left, right):
        Pattern.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, text, env=None):
        return self.left(text, env) ^ self.right(text, env)
    def __repr__(self):
        return "%s ^ %s" % (repr(self.left), repr(self.right))

class PatternOr(Pattern):
    """Disjunction between patterns."""
    def __init__(self, left, right):
        Pattern.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, text, env=None):
        return self.left(text, env) or self.right(text, env)
    def __repr__(self):
        return "%s | %s" % (repr(self.left), repr(self.right))

class PatternInvert(Pattern):
    """Negation of the patterns."""
    def __init__(self, term):
        Pattern.__init__(self)
        self.term = term
    def __call__(self, text, env=None):
        return not self.term(text, env)
    def __repr__(self):
        return "~%s" % repr(self.term)

class PatternFunction(Pattern):
    """Negation of the pattern."""
    def __init__(self, function):
        Pattern.__init__(self)
        self.function = function
    def __call__(self, text, env=None):
        return self.function(text, env)
    def __repr__(self):
        return "FunctionTrigger(%s)" % self.function

class PatternRegex(Pattern):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)
    def __call__(self, text, env=None):
        return self.pattern.search(text)
    
def check(patterns, text, env=None):
    for pattern, action in patterns:
        if pattern(text, env):
            return action(env)