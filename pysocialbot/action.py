

class Action():
    """Action base."""
    def __init__(self):
        pass
    def __call__(self, env):
        """
        It must return True or False.
        If it returned False,the daemon will execute again.
        """
        return True
    def __add__(self, other):
        return ActionCombine(self, other)
    def __and__(self, other):
        return ActionAnd(self, other)
    def __or__(self, other):
        return ActionOr(self, other)
    def __repr__(self):
        return "Action"
    def execute(self, env):
        """synonymous with __call__."""
        return self.__call__(env)
    def otherwise(self, action):
        """synonymous with __or__."""
        return ActionOr(self, action)

class ActionCombine(Action):
    """It does two actions."""
    def __init__(self, left, right):
        Action.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, env):
        left = self.left(env)
        right = self.right(env)
        return left and right
    def __repr__(self):
        return "%s + %s" % (repr(self.left), repr(self.right))

class ActionAnd(Action):
    """If first action returns True, It returns second action.
    otherwise, it returns False."""
    def __init__(self, left, right):
        Action.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, env):
        return self.left(env) and self.right(env)
    def __repr__(self):
        return "%s & %s" % (repr(self.left), repr(self.right))

class ActionOr(Action):
    """If first action returns False, it returns second action.
    otherwise, it returns True."""
    def __init__(self, left, right):
        Action.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, env):
        return self.left(env) or self.right(env)
    def __repr__(self):
        return "%s | %s" % (repr(self.left), repr(self.right))

class Call(Action):
    """Call specified function."""
    def __init__(self, function):
        Action.__init__(self)
        self.function = function
    def __call__(self, env):
        return self.function(env)
    def __repr__(self):
        return self.function.__doc__