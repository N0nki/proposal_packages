# coding: utf-8

"""
author Mio Kinno
date 2017.6.21
branch py3
file directed_graph.py

graphillionで有向グラフのパス列挙を行えるようにする


# 除外すべきグラフの要素
* rule1
  スタートノードに流入するリンクを除外する

* rule2
  rule1で除外したリンクの構成ノード以外のノードのなかで流入するリンクの数が2以上のノードに着目する
  そのノードに流入するリンク2つから構成されるすべてのサブグラフを除外する
  着目しているノードに流入するリンク数をnとすれば除外するサブグラフはnC2個存在する


 # 使い方
1. NetworkXの有向グラフオブジェクトを作成する
   辺重みは付けても付けなくてもよい
2. GraphSet.set_universe(G.edges())を実行してGraphillionにグラフを読み込ませる
3. directed_paths(G, s, t)を実行する
"""

from itertools import combinations

from graphillion import GraphSet
import networkx as nx

def internal_edges(DiGraph, start_node):
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

def two_internal_edges_subgraph(DiGraph, node):
    """
    rule2

    arguments:
    * DiGraph(networkx directed Graph object)
    * node(node label)

    returns:
    * subgraphs(list)
      rule2にあてはまるサブグラフを格納したリスト
    """
    internal_links = [link[0] for link in internal_edges(DiGraph, node)]
    if len(internal_links) < 2:
        return
    subgraphs = [[link1, link2] for link1,link2 in combinations(internal_links, 2)]
    return subgraphs

def invalid_direction_elms(DiGraph, start_node):
    """
    rule1とrule2の結果をまとめる

    arguments:
    * DiGraph(networkx directed Graph object)
    * start_node(node label)

    returns:
    * elms(list)
      rule1とrule2にあてはまる除外すべきグラフの要素を格納したリスト
    """
    rule1 = internal_edges(DiGraph, start_node)
    rule1_nodes = [start_node] + DiGraph.predecessors(start_node)
    rule2_nodes = set(DiGraph.nodes()) - set(rule1_nodes)
    elms = []
    for node in rule2_nodes:
        rule2 = two_internal_edges_subgraph(DiGraph, node)
        if rule2 is None: continue
        for subgraph in rule2:
            elms.append(subgraph)
    if len(rule1) == 0:
        return elms
    else:
        for e in rule1:
            elms.append(e)
        return elms

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
    elms = invalid_direction_elms(DiGraph, start_node)
    di_paths = di_paths.excluding(GraphSet(elms))
    return di_paths

if __name__ == "__main__":
    # 動作確認
    G = nx.DiGraph(data=[("a","b"), ("a","d"), ("b","c"), ("b","e"),
                         ("d","c"), ("d", "e"), ("e","f"), ("f","c")])
    GraphSet.set_universe(G.edges())
    print(internal_edges(G, "b"))
    print(two_internal_edges_subgraph(G, "c"))
    print(invalid_direction_elms(G, "b"))
    print(directed_paths(G, "b", "c"))
    print("the following results are directed_paths of start node to target node")
    for path in directed_paths(G, "b", "c"):
        print(path)
