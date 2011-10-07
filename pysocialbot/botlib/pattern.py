"""
Pattern-to-response chatter.
This contains chatter utility.
"""
import re
import random
from pysocialbot import trigger

class Pattern(trigger.Trigger):
    def __init__(self, wrap=trigger.Trigger, *args, **kwargs):
        trigger.Trigger.__init__(self)
        self.wrap = wrap
        wrap.__init__(self, *args, **kwargs)
    def __call__(self, text, env):
        self.wrap(self, env)

class Regex(Pattern):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)
    def __call__(self, text, env):
        return self.pattern.search(text)

class SubPattern:
    def __init__(self, patterns):
        self.patterns = patterns
    def __call__(self, text, env):
        return check(self.patterns, text, env)

ISREPLY = Regex("^@\w+")
ISMENTION = Regex("@\w+")

def choice(*args):
    return lambda text, env: random.choice(args)

def check(patterns, text, env=None):
    for pattern, action in patterns:
        if pattern(text, env):
            return action(text, env)