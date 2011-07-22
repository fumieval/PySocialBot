"""
PySocialBot daemon
"""
from __future__ import unicode_literals
from pysocialbot.settings import RUN_INTERVAL
from pysocialbot import Object

import datetime
import random
import time
import pickle
import itertools

DT = datetime.timedelta

def dailysection(hour=0, minute=0, second=0, microsecond=0):
    """section with daily cycle."""
    return datetime.datetime(datetime.MINYEAR,
                             month=1, day=1,
                             hour=hour, minute=minute, second=second,
                             microsecond=microsecond)

def yearlysection(month=1, day=1, hour=0, minute=0, second=0):
    """section with yearly cycle."""
    return datetime.datetime(datetime.MINYEAR,
                             month=month, day=day,
                             hour=hour, minute=minute, second=second)

def nowf():
    """formated current time."""
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

def newstate(env, trigger, state, action):
    """do action and return state."""
    if trigger(env):
        if state:
            return True
        else:
            result = action(env)
            print("%s\t%s -> [%s] => %s" % (nowf(),
                                            repr(trigger), repr(action),
                                            repr(result)))
            return bool(result)
    else:
        return False

class Daemon():
    
    """
    Daemon class.
    Do actions if trigger is effected.
    """
    
    def __init__(self, env=Object()):
        self.env = env
        self.env.daemon = self
        self.trigger = {}
        self.state = {}
        self.queue = []
        self.hooks = []

    def put(self, trigger, action):
        """Put trigger and action"""
        self.queue.append((trigger, action))

    def __len__(self):
        return len(self.trigger)

    def resetstate(self):
        """reset trigger state."""
        for key in self.trigger:
            self.state[key] = False

    def dumpstate(self, filename):
        """dump trigger state."""
        pickle.dump(self.state, filename)

    def loadstate(self, filename):
        """load trigger state."""
        for key, val in itertools.ifilter(lambda x: x[0] in self.trigger,
                                          pickle.load(filename).items()):
            self.state[key] = val

    def run(self):
        """run daemon."""
        print("%s\tDaemon Start." % nowf())
        
        for hook in self.hooks:
            hook(self.env)
        
        while True:
            for key in self.trigger:
                self.state[key] = newstate(self.env, key,
                                           self.state[key],
                                           self.trigger[key])
            self.queue = \
            [(k, x) for k, x in self.queue if not (k(self.env) and x(self.env))]
            
            time.sleep(RUN_INTERVAL)

class Trigger():
    
    """Trigger class."""
    def __init__(self):
        pass
    def __call__(self, env):
        """Always returns true."""
        return True
    def __and__(self, other):
        return TriggerAnd(self, other)
    def __xor__(self, other):
        return TriggerXor(self, other)
    def __or__(self, other):
        return TriggerOr(self, other)
    def __invert__(self):
        return TriggerInvert(self)
    def __cmp__(self, other):
        return cmp(repr(self), repr(other)) 
    def __hash__(self):
        return repr(self).__hash__()
    def __repr__(self):
        return "Trigger()"
    def check(self, env):
        """synonymous with __call__."""
        return self(env)
    def invert(self):
        """synonymous with __invert__."""
        return self.__invert__()

class TriggerAnd(Trigger):
    """Intersection between triggers."""
    def __init__(self, left, right):
        Trigger.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, env):
        return self.left(env) and self.right(env)
    def __repr__(self):
        return "%s & %s" % (repr(self.left), repr(self.right))

class TriggerXor(Trigger):
    """Exclusive intersection between triggers."""
    def __init__(self, left, right):
        Trigger.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, env):
        return self.left(env) ^ self.right(env)
    def __repr__(self):
        return "%s ^ %s" % (repr(self.left), repr(self.right))

class TriggerOr(Trigger):
    """Disjunction between triggers."""
    def __init__(self, left, right):
        Trigger.__init__(self)
        self.left = left
        self.right = right
    def __call__(self, env):
        return self.left(env) or self.right(env)
    def __repr__(self):
        return "%s | %s" % (repr(self.left), repr(self.right))

class TriggerInvert(Trigger):
    """Negation of the trigger."""
    def __init__(self, term):
        Trigger.__init__(self)
        self.term = term
    def __call__(self, env):
        return not self.term(env)
    def __repr__(self):
        return "~%s" % repr(self.term)

class FunctionTrigger(Trigger):
    """Negation of the trigger."""
    def __init__(self, function):
        Trigger.__init__(self)
        self.function = function
    def __call__(self, env):
        return self.function(env)
    def __repr__(self):
        return "FunctionTrigger(%s)" % repr(self.function)

class Time(Trigger):
    """Delay trigger."""
    def __init__(self, target=datetime.datetime.today()):
        Trigger.__init__(self)
        self.time = target
    def __call__(self, env):
        return datetime.datetime.today() >= self.time
    def __repr__(self):
        return "Time(%s)" % repr(self.time)

class Delay(Time):
    """Delay trigger."""
    def __init__(self, offset=datetime.timedelta()):
        Trigger.__init__(self)
        self.time = datetime.datetime.today() + offset
    def __call__(self, env):
        return datetime.datetime.today >= self.time

class Regular(Trigger):
    """Trigger effects at regular intervals."""
    def __init__(self, span, offset=datetime.timedelta()):
        """
        Keyword arguments:
        span -- interval.
        offset -- time offset.
        """
        Trigger.__init__(self)
        self.span = span
        self.offset = offset
    def __call__(self, env):
        target = datetime.datetime.today() - self.offset
        return ((target.hour * 60 + target.minute) * 60 +
                target.second) % self.span == 0
    def __repr__(self):
        return "Regular(%d, %s)" % (self.span, str(self.offset))

class Hourly(Trigger):
    """Trigger effects hourly."""
    def __init__(self, offset=datetime.timedelta()):
        Trigger.__init__(self)
        self.offset = offset
    def __call__(self, env):
        return (datetime.datetime.today() - self.offset).minute == 0
    def __repr__(self):
        return "Hourly(%s)" % str(self.offset)

class Daily(Trigger):
    """Trigger effects daily."""
    def __init__(self, offset=datetime.timedelta()):
        Trigger.__init__(self)
        self.offset = offset
    def __call__(self, env):
        return (datetime.datetime.today() - self.offset).hour == 0
    def __repr__(self):
        return "Daily(%s)" % str(self.offset)

class Weekly(Trigger):
    """Trigger effects weekly."""
    def __init__(self, offset=datetime.timedelta()):
        Trigger.__init__(self)
        self.offset = offset
    def __call__(self, env):
        return (datetime.datetime.today()-self.offset).weekday() == 0
    def __repr__(self):
        return "Weekly(%s)" % str(self.offset)

class Monthly(Trigger):
    """Trigger effects monthly."""
    def __init__(self, day, offset=datetime.timedelta()):
        Trigger.__init__(self)
        self.day = day
        self.offset = offset
    def __call__(self, env):
        return (datetime.datetime.today() - self.offset).day == self.day
    def __repr__(self):
        return "Monthly(%02d, %s)" % (self.day, str(self.offset))

class Yearly(Trigger):
    """Trigger effects yearly."""
    def __init__(self, month, offset=datetime.timedelta()):
        Trigger.__init__(self)
        self.month = month
        self.offset = offset
    def __call__(self, env):
        return (datetime.datetime.today() - self.offset).month == self.month
    def __repr__(self):
        return "Yearly(%02d, %s)" % (self.month, str(self.offset))

class InDailyPeriod(Trigger):
    """Trigger effects between specified section."""
    def __init__(self, begin, end):
        Trigger.__init__(self)
        self.begin = begin.replace(year=datetime.MINYEAR, month=1, day=1)
        self.end = end.replace(year=datetime.MINYEAR, month=1, day=1)
    def __call__(self, env):
        now = datetime.datetime.today().replace(year=datetime.MINYEAR,
                                                month=1, day=1)
        return (self.begin == None or self.begin <= now) and \
               (self.end == None or self.end >= now)
    def __repr__(self):
        return "InDailySection(%s, %s)" % (str(self.begin).split()[1],
                                           str(self.end).split()[1])

class InYearlyPeriod(Trigger):
    """Trigger effects between specified section."""
    def __init__(self, begin, end):
        Trigger.__init__(self)
        self.begin = begin.replace(year=datetime.MINYEAR)
        self.end = end.replace(year=datetime.MINYEAR)
    def __call__(self, env):
        now = datetime.datetime.today().replace(year=datetime.MINYEAR)
        return (self.begin == None or self.begin <= now) and \
               (self.end == None or self.end >= now)
    def __repr__(self):
        return "InDailySection(%s, %s)" % (str(self.begin), str(self.end))

class Randomly(Trigger):
    """Trigger effects randomly."""
    def __init__(self, probability=0):
        Trigger.__init__(self)
        self.probability = probability
    def __call__(self, env):
        return random.random() < self.probability
    def __repr__(self):
        return "Randomly(%s)" % str(self.probability)
