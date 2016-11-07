# coding: utf-8

"""
author Mio Kinno
date 2016.11.1
branch master
file directed_path_v3.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す

# 動作概要
仮想ノードの追加を1つだけにする
"""

from itertools import combinations
from collections import defaultdict

from graphillion import GraphSet

def same_nodes_link_dict(edgelist):
    """
    キーが(i,j)、値が[(i,j,cost1),(j,i,cost2)]の辞書を返す
    """
    d = defaultdict(list)
    for i,j,cost in edgelist:
        d[(i,j)].append((i,j,cost))
        if (j,i) in d:
            del d[(i,j)]
            d[(j,i)].append((i,j,cost))
    return d

def append_virtual_nodes(edgelist):
    """
    """
    d = same_nodes_link_dict(edgelist)
    virtual_nodes_Graph = []
    for link1,link2 in d.values():
        i, j, cost = link2[0], link2[1], link2[2]
        v = i + "_" + j
        virtual_nodes_Graph += [link1, (i,v,cost), (v,j,0)]
    return virtual_nodes_Graph

def get_virtual_nodes(edgelist):
    """
    """
    d = same_nodes_link_dict(edgelist)
    virtual_nodes = []
    for link1,link2 in d.values():
        i, j, cost = link2[0], link2[1], link2[2]
        v = i + "_" + j
        virtual_nodes.append(v)
    return virtual_nodes

def get_original_nodes(edgelist):
    """
    仮想ノード追加前のグラフのノードのリストを返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    returns:
    * nodes(node list)
      仮想ノード追加前のグラフのノードのリスト
    """
    edges = [[i,j] for i,j,cost in edgelist]
    return set(reduce(lambda x,y: x + y, edges))

def get_predecessor_nodes(edgelist, node):
    """
    """
    virtual_nodes = get_virtual_nodes(edgelist)
    predecrssor_nodes = []
    for v in virtual_nodes:
        i, j = v.split("_")
        if node == i:
            predecrssor_nodes.append(j)
        elif node == j:
            predecrssor_nodes.append(v)
    return predecrssor_nodes

def internal_links(edgelist, node):
    """
    rule1
    """
    predecrssors = get_predecessor_nodes(edgelist, node)
    il = [[(p, node)] for p in predecrssors]
    return il

def two_internal_links_subgraph(edgelist, node):
    """
    rule2
    """
    il = [link[0] for link in internal_links(edgelist, node)]
    if len(il) < 2:
        return
    subgraphs = [[link1, link2] for link1,link2 in combinations(il, 2)]
    return subgraphs

def directed_paths(edgelist, start_node, target_node):
    """
    """
    rule1 = internal_links(edgelist, start_node)
    rule2_nodes = get_original_nodes(edgelist) - {start_node, target_node}
    elms = [link for link in rule1]
    for node in rule2_nodes:
        rule2 = two_internal_links_subgraph(edgelist, node)
        if rule2 is None: continue
        for subgraph in rule2:
            elms.append(subgraph)
    elms = GraphSet(elms)
    di_paths = GraphSet.paths(start_node, target_node).excluding(elms)
    return di_paths

if __name__ == "__main__":
    # 動作確認
    edgelist = [(u"1",u"2",1),(u"1",u"3",2),(u"2",u"3",3),(u"2",u"4",4),(u"3",u"4",5),
                (u"2",u"1",-1),(u"3",u"1",-2),(u"3",u"2",-3),(u"4",u"2",-4),(u"4",u"3",-5)]

    GraphSet.set_universe(append_virtual_nodes(edgelist))
    # print append_virtual_nodes(edgelist)
    # print "virtual_nodes", get_virtual_nodes(edgelist)
    # print "predecrssor_nodes", get_predecessor_nodes(edgelist, u"4")
    # print "internal_links", internal_links(edgelist, u"4")
    # print "two_internal_links_subgraph", two_internal_links_subgraph(edgelist, u"4")
    for path in directed_paths(edgelist, u"2", u"3"):
        print path
