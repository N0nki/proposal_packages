"""
Author: Mio Kinno
Date: 2018.6.11
File: graphillion_utils.py

graphillionを操作しているときによく使う機能をまとめたモジュール
"""

import random
from graphillion import GraphSet

def degree(node):
    """
    nodeの字数を返す

    arguments:
    * node(node label)

    returns:
    * degree(int)
      nodeの次数
    """

    return len(GraphSet({}).including(node).graph_size(1))

def flatten_paths(paths):
    """
    パス集合を平滑化してリンクを要素とするリストを返す
    """

    return [edge for path in paths for edge in path]

def min_hop(terminal):
    """
    2頂点間を結ぶパスの最小ホップ数を求める
    """

    return len(next(GraphSet.paths(terminal[0], terminal[1]).min_iter()))

def max_hop(terminal):
    """
    2頂点間を結ぶパスの最大ホップ数を求める
    """

    return len(next(GraphSet.paths(terminal[0], terminal[1]).max_iter()))

def get_min_hop_paths(paths, terminal):
    """
    最小ホップ数のパス集合を返す

    arguments:
    * paths(graphset)
    * terminal(tuple (s, t), including start and target node)

    returns:
    * min_hop_paths(graphset)
    """

    return paths.graph_size(min_hop(terminal))

def excluding_multi_elms(graphset, elms):
    """
    複数のグラフ要素をグラフセットから削除する

    arguments:
    * graphset(graphset)
    * elms(graph elements, node, edge, graph, graphset)

    returns:
    * graphset(graphset)
    """

    for elm in elms:
        graphset = graphset.excluding(elm)

    return graphset

def select_sleep_nodes(nodes, terminal, num):
    """
    スリープするノードを決定する

    arguments:
    * nodes(node list)
    * terminal(tuple (s, t), including start and target node)
    * num(int)
      スリープするノードの数
    """

    candidate = set(nodes) - set(terminal)
    return random.sample(candidate, k=num)

def hamming(graphset, G, upper_limit):
    pass

def get_similar_paths(edgelist, terminal, path, upper_limit):
    pass
