"""
PySocialBot daemon
"""
from __future__ import unicode_literals

from pysocialbot import trigger
from pysocialbot.settings import RUN_INTERVAL
from pysocialbot.struct import Object

import datetime
import time
import cPickle as pickle
import sys
from itertools import ifilter

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
            if env.daemon.debug:
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
        self.env.flag = {}
        self.trigger = {}
        self.state = {}
        self.queue = []
        self.hooks = []
        self.debug = False

    def push(self, trigger, action):
        """Put trigger and action"""
        self.queue.append((trigger, action))

    def __len__(self):
        return len(self.trigger)

    def reset(self):
        """reset trigger state."""
        for key in self.trigger:
            self.state[key] = False

    def dump(self, filename):
        """dump trigger state."""
        pickle.dump(self.state, filename)

    def load(self, filename):
        """load trigger state."""
        for key, value in ifilter(lambda x: x[0] in self.trigger,
                                  pickle.load(filename).iteritems()):
            self.state[key] = value

    def setflag(self, name, value):
        self.env.flag[name] = value
    
    def getflag(self, name):
        return self.env.flag[name]
    
    def run(self):
        """run daemon."""
        if self.debug:
            print("%s\tDaemon Start." % nowf())
        
        for hook in self.hooks:
            hook(self.env)
        
        while True:
            for key in self.trigger:
                self.state[key] = newstate(self.env, key,
                                           self.state[key],
                                           self.trigger[key])
            self.queue = filter(lambda i: not (i[0](self.env) and i[1](self.env)), self.queue)
            sys.stdout.flush()
            time.sleep(RUN_INTERVAL)

class Flag(trigger.Trigger):
    def __init__(self, name):
        self.name = name

    def __call__(self, env):
        return env[self.name]