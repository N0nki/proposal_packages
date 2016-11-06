# coding: utf-8

"""
author Mio Kinno
date 2016.10.24
file directed_path_v3.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す

# 動作概要
v2の改良版
除外すべき要素からなるグラフセットを作成しGraphSet.excludingの引数に渡すように変更
要素はリンクであってもサブグラフとして除外する
Graphillionが扱うリンクは(i,j)の形式だがこれを[(i,j)]とすることでサブグラフとすることができる
"""

from itertools import combinations

from graphillion import GraphSet
import networkx as nx

def start_node_internal_links(DiGraph, start_node):
    """
    rule1

    arguments:
    * DiGraph(networkx directed Graph object)
    * start_node(start node label)

    returns:
    * internal_links(list)
      rule1にあてはまるリンクからなるサブグラフを格納したリスト
    """
    internal_links = [[(predecessor, start_node)]\
                      for predecessor in DiGraph.predecessors_iter(start_node)]
    return internal_links

def subgraph_by_two_internal_links(DiGraph, node):
    """
    rule2

    arguments:
    * DiGraph(networkx directed Graph object)
    * node(node label)

    returns:
    * subgraphs(list)
      rule2にあてはまるサブグラフを格納したリスト
    """
    internal_links = [link[0] for link in start_node_internal_links(DiGraph, node)]
    if len(internal_links) < 2:
        return
    subgraphs = [[link1, link2] for link1,link2 in combinations(internal_links, 2)]
    return subgraphs

def collect_invalid_direction_elms(DiGraph, start_node):
    """
    rule1とrule2の結果をまとめる

    arguments:
    * DiGraph(networkx directed Graph object)
    * start_node(node label)

    returns:
    * elms(list)
      rule1とrule2にあてはまる除外すべきグラフの要素を格納したリスト
    """
    rule1 = start_node_internal_links(DiGraph, start_node)
    rule1_nodes = [start_node] + DiGraph.predecessors(start_node)
    rule2_nodes = set(DiGraph.nodes()) - set(rule1_nodes)
    elms = []
    for node in rule2_nodes:
        rule2 = subgraph_by_two_internal_links(DiGraph, node)
        if rule2 is None: continue
        for subgraph in rule2:
            elms.append(subgraph)
    if len(rule1) == 0:
        return elms
    for e in rule1:
        return elms.append(e)

def directed_paths(DiGraph, start_node, target_node):
    """
    有効性を考慮したパスだけを含むグラフセットを返す

    arguments:
    * DiGraph(networkx directed Graph object)
    * start_node(start node label)
    * target_node(target node label)

    returns:
    * di_paths(graphillion.GraphSet)
      有効性を考慮したパスだけを含むグラフセット
    """
    di_paths = GraphSet.paths(start_node, target_node)
    elms = collect_invalid_direction_elms(DiGraph, start_node)
    di_paths = di_paths.excluding(GraphSet(elms))
    return di_paths

if __name__ == "__main__":
    # 動作確認
    G = nx.DiGraph(data=[("a","b"), ("a","d"), ("b","c"), ("b","e"),
                         ("d","c"), ("d", "e"), ("e","f"), ("f","c")])
    GraphSet.set_universe(G.edges())
    print start_node_internal_links(G, "b")
    print subgraph_by_two_internal_links(G, "c")
    print collect_invalid_direction_elms(G, "b")
    print directed_paths(G, "b", "c")
    print "the following results are directed_paths of start node to target node"
    for path in directed_paths(G, "b", "c"):
        print path

