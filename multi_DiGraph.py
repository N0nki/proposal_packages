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
        virtual_nodes_graph = self.append_virtual_nodes()
        GraphSet.set_universe(virtual_nodes_graph)

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
        仮想ノードを追加したグラフの辺のリストを返す

        returns:
        * virtual_nodes_graph(edge list)
          仮想ノードを追加したグラフの重み付き辺のタプルを要素とするリスト
        """
        d = self.edges_table()
        virtual_nodes_graph = []
        for e1,e2 in d.values():
            i, j, w = e2[0], e2[1], e2[2]
            v = (i,j)
            virtual_nodes_graph += [e1, (i,v,w), (v,j,0)]
        return virtual_nodes_graph

    def universe(self):
        return GraphSet.universe()

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

    def virtual_nodes_iter(self):
        pass

    def original_nodes(self):
        """
        仮想ノード追加前のグラフのノードのリストを返す

        returns:
        * o_nodes(node set)
          仮想ノード追加前のグラフのノードを格納したリスト
        """
        edges = [[i,j] for i,j,w in self.edgelist]
        return set(reduce(lambda x,y: x + y, edges))

    def original_nodes_iter():
        pass

    def predecessor_nodes(self, node):
        """
        nodeへの流入リンク(predecessor, node)を構成するノードpredecessorを返す

        returns:
        * predecessors(node list)
          predecessorノードを格納したリスト
        """
        v_nodes = self.virtual_nodes()
        predecessors = []
        for i,j in v_nodes:
            if node == i:
                predecessors.append(j)
            if node == j:
                predecessors.append((i,j))
        return predecessors

    def predecessors_iter(self, node):
        """
        nodeへの流入リンク(predecessor, node)を構成するノードpredecessorを返す

        yields:
        * predecessors
          predecessorノードを格納したリスト
        """
        v_nodes = self.virtual_nodes()
        for i,j in v_nodes:
            if node == i:
                yield j
            if node == j:
                yield (i,j)

    def neighbor_nodes(self, node):
        pass

    def neighbors_iter(self, node):
        pass

    def degree(self, node):
        return len(GraphSet({}).graph_size(1).including(node))

if __name__ == "__main__":
    edgelist = [(1,2,1),(1,3,2),(2,3,3),(2,4,4),(3,4,5),
                (2,1,-1),(3,1,-2),(3,2,-3),(4,2,-4),(4,3,-5)]
    G = MultiDiGraph(edgelist)
    print("Universe", G.universe())
    print("edges_table", G.edges_table())
    print("virtual_nodes", G.virtual_nodes())
    print("degree", G.degree(1))
    print("original_nodes", G.original_nodes())
    for p in G.predecessors_iter(1):
        print(p)
