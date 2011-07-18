# coding: utf-8
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
    
    def extract(self, source, pick):
        total = {}
        for item in itertools.ifilter(lambda x: x in self.table, source):
            for key, value in self.table[item].items():
                if not key in total:
                    total[key] = 0
                total[key] += value
        if total == {}:
            return [], 0
        result = list(total.iteritems())
        result.sort(key=lambda x: -x[1])
        
        pick_rest = pick #抽出する量
        samples = []
        for group in itertools.imap(lambda x: list(x[1]),
                                    itertools.groupby(result, key=lambda x: -x[1])):
            if len(group) >= pick_rest:
                samples.extend(random.sample(group, pick_rest))
                break
            else:
                samples.extend(group)
                pick_rest -= len(group)
                if pick_rest <= 0:
                    break
        return (map(lambda x: x[0], samples),
                sum(itertools.imap(lambda x: x[1], samples)) / len(samples))
    
    def load(self, file):
        self.table = pickle.load(file)
        
    def dump(self, file):
        pickle.dump(self.table, file)
           