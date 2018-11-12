import csv
from copy import deepcopy
from collections import deque
from random import shuffle

class Pairings():
    def __init__(self):
        self.pairs = set()
        self.new_pairs = set()
        self.names = []
        self.get_pairs()
        self.get_names()
        shuffle(self.names) # trying to do the same order each time will iteratively slow the depth first search
        self.used = set()
        self.n = len(self.names)

    def get_pairs(self):
        with open('pairs.csv', 'rb') as f:
            reader = csv.reader(f)
            for line in reader:
                self.pairs.add(tuple((line[0], line[1])))

    def add_pair(self, pair):
        self.pairs.add(pair)
        self.new_pairs.add(pair)

    def get_names(self):
        with open('names.csv', 'rb') as f:
            reader = csv.reader(f)
            for line in reader:
                self.names.append(line[0])

    def copy(self):
        return deepcopy(self)

    def get_successors(self, name):
        for other_name in self.names:
            if other_name != name and (name, other_name) not in self.pairs and (other_name, name) not in self.pairs and other_name not in self.used and name not in self.used:
                new_obj = self.copy()
                new_obj.add_pair((name, other_name))
                new_obj.used.add(name)
                new_obj.used.add(other_name)
                yield new_obj
                
    def make_pairs_helper(self):
        while self.names:
            name = self.names.pop()
            for succ in self.get_successors(name):
                if len(succ.new_pairs) == succ.n / 2:
                    return succ
                else:
                    succ = succ.make_pairs_helper()
                    if succ is not None:
                        return succ
        
        return None

    def make_pairs(self):
        new_obj = self.make_pairs_helper()
        new_obj.write_pairs()
        new_obj.write_new_pairs()
    
    def write_pairs(self):
        with open('pairs.csv', 'w') as f:
            writer = csv.writer(f)
            while self.pairs:
                pair = self.pairs.pop()
                writer.writerow([pair[0], pair[1]])

    def write_new_pairs(self):
        with open('new_pairs.csv', 'w') as f:
            writer = csv.writer(f)
            while self.new_pairs:
                pair = self.new_pairs.pop()
                writer.writerow([pair[0], pair[1]])

pairings = Pairings()
pairings.make_pairs()