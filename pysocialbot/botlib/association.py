"""
PySocialBot Botlib :: Association Library
"""

import itertools
import random
import cPickle as pickle

class Association:
    def __init__(self):
        self.table = {}
        
    def learn(self, source, target):
        for i, j in itertools.product(source, target):
            if not i in self.table:
                self.table[i] = {}
            if not j in self.table[i]:
                self.table[i][j] = 0
            self.table[i][j] += 1
    
    def extract(self, source):
        total = {}
        for item in itertools.ifilter(lambda x: x in self.table, source):
            for key, value in self.table[item].items():
                if not key in total:
                    total[key] = 0
                total[key] += value
        if total == {}:
            return [], 0
        maxvalue = max(total.itervalues())
        return map(lambda xs: xs[0],
                   itertools.ifilter(lambda xs: xs[1] == maxvalue, total.iteritems())), maxvalue
    
    def load(self, file):
        self.table = pickle.load(file)
        
    def dump(self, file):
        pickle.dump(self.table, file)