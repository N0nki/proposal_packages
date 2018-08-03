"""
Author: Mio Kinno
Date: 2018.6.11
File: graphillion_utils.py

graphillionを操作しているときによく使う機能をまとめたモジュール
"""

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

def hamming(graphset, G, upper_limit):
    pass

def get_similar_paths(edgelist, terminal, path, upper_limit):
    pass
