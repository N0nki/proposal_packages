"""
有向グラフの有向辺を考慮してパス列挙
"""

from itertools import permutations
import networkx as nx
from pandas import DataFrame
from graphillion import GraphSet
import utils
utils.expand_load_path(__file__)
import directed_graph as dg

edgelist = [("A","B",2), ("A","D",1),
            ("B","E",10), ("B","D",3),
            ("C","A",4), ("C","F",5),
            ("D","C",2), ("D","F",8), ("D","G",4),
            ("E","G",6),
            ("G","F",1)]

metric_table = {(i,j): w for i,j,w in edgelist}

pos = {"A": (-2,0), "B": (-1,1), "C": (-1,-1),
       "D": (0,0), "E": (1,1), "F": (1,-1), "G": (2,0)}

G = nx.DiGraph()
G.add_weighted_edges_from(edgelist)

GraphSet.set_universe(G.edges())

# 全頂点間のパスの本数を求める
all_results = []
for s,t in permutations(G.nodes(), 2):
    paths = dg.directed_paths(G, s, t)
    all_results.append({"start":s, "target":t, "number of paths": len(paths)})
    # print(s, t, len(paths))
print(DataFrame(all_results, columns=["start", "target", "number of paths"]))
