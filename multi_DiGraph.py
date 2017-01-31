# coding: utf-8

"""
NetworkX multiDiGraph implemented by Graphillion
"""

from itertools import combinations
from collections import defaultdict
import math
import random

from graphillion import GraphSet

class MultiDiGraph:
    """
    双方向リンクを持つグラフ
    """
    def __init__(self, edgelist):
        self.edgelist = edgelist

    def edges_table(self):
        d = defaultdict(list)
        for i,j,w in edgelist:
            d[(i,j)].append((i,j,w))
            if (j,i) in d:
                del d[(i,j)]
                d[(j,i)].append((i,j,w))
        return d

if __name__ == "__main__":
    edgelist = [(1,2,1),(1,3,2),(2,3,3),(2,4,4),(3,4,5),
                (2,1,-1),(3,1,-2),(3,2,-3),(4,2,-4),(4,3,-5)]
    G = MultiDiGraph(edgelist)
    print G.edges_table()
