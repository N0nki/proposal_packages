# coding: utf-8

"""
NetworkX like multiDiGraph implemented by Graphillion
"""

from __future__ import print_function
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
        """
        キーが(i,j)、値が[(i,j,cost1),(j,i,cost2)]の辞書を返す

        returns:
        * d(defaultdict)
          key: (i,j)
          value: [(i,j,cost1),(j,i,cost2)]
        """
        d = defaultdict(list)
        for i,j,w in self.edgelist:
            d[(i,j)].append((i,j,w))
            if (j,i) in d:
                del d[(i,j)]
                d[(j,i)].append((i,j,w))
        return d

    def append_virtual_nodes(self):
        """

        """
        d = self.edges_table()
        virtual_nodes_graph = []
        for e1,e2 in d.values():
            i, j, w = e2[0], e2[1], e2[2]
            v = (i,j)
            virtual_nodes_graph += [e1, (i,v,w), (v,j,0)]
        return virtual_nodes_graph

    def virtual_nodes(self):
        """
        仮想ノードのリストを返す

        returns:
        * v_nodes(nodes list)
          仮想ノードを格納したリスト
        """
        d  = self.edges_table()
        v_nodes = []
        for e1,e2 in d.values():
            i, j, w = e2[0], e2[1], e2[2]
            v_nodes.append((i,j))
        return v_nodes

    def original_nodes(self):
        """
        仮想ノード追加前のグラフのノードのリストを返す

        returns:
        * o_nodes(node set)
          仮想ノード追加前のグラフのノードを格納したリスト
        """
        edges = [[i,j] for i,j,w in self.edgelist]
        return set(reduce(lambda x,y: x + y, edges))

if __name__ == "__main__":
    edgelist = [(1,2,1),(1,3,2),(2,3,3),(2,4,4),(3,4,5),
                (2,1,-1),(3,1,-2),(3,2,-3),(4,2,-4),(4,3,-5)]
    G = MultiDiGraph(edgelist)
    print("edges_table", G.edges_table())
    print("append_virtual_nodes", G.append_virtual_nodes())
    print("virtual_nodes", G.virtual_nodes())
    # print("original_nodes", G.original_nodes())
    G.original_nodes()
