"""
PySocialBot Botlib :: Association Library
"""

import itertools
import random

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
        S = sum(total.itervalues())
        result = filter(lambda x: x[0] == S, total.iteritems())
        if result:
            return random.choice(result)[1]