# coding: utf-8

"""
author Mio Kinno
date 2016.10.31
branch single_virtual_node
file directed_path_v3.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す

# 動作概要
仮想ノードの追加を1つだけにする
"""

from itertools import combinations

from graphillion import GraphSet
