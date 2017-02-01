# coding: utf-8

"""
author Mio Kinno
date 2017.2.1
branch master
file directed_link_two_virtual_nodes.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す

# 動作概要
branch two_virtual_nodes_NetworkXと動作は同じだが
NetworkXを一切使用しない実装
仮想ノードを2個追加する
不要なサブグラフのグラフセットの作成をまとめて行うことで高速化
directed_link.pyと同様の操作を実現する


# 使い方
1. グラフの重み付きリンクのタプル(i,j,cost)を要素とするリストedgelistを用意する。
2. read_edgelist(edgelist)を実行してモジュールにedgelistを読み込ませる
3. GraphSet.set_universe(append_virtual_nodes())を実行してGraphillionに仮想ノードを追加したグラフを読み込ませる
4. directed_paths(start_node, target_node)を実行する
"""

from itertools import combinations
from collections import defaultdict

from graphillion import GraphSet

def read_edgelist(data):
    """
    グローバル変数edgelistを設定する

    arguments:
    * data(list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト
    """
    global edgelist
    edgelist = data

def edges_table():
    """
    キーが(i,j)、値が[(i,j,cost1),(j,i,cost2)]の辞書を返す

    returns:
    * d(defaultdict)
      key: (i,j)
      value: [(i,j,cost1),(j,i,cost2)]
    """
    global edgelist
    d = defaultdict(list)
    for i,j,cost in edgelist:
        d[(i,j)].append((i,j,cost))
        if (j,i) in d:
            del d[(i,j)]
            d[(j,i)].append((i,j,cost))
    return d

def append_virtual_nodes():
    """
    仮想ノードを追加したグラフの辺のリストを返す

    returns:
    * virtual_nodes_graph(edge list)
      仮想ノードを追加したグラフの重み付き辺のタプルを要素とするリスト
    """
    global edgelist
    virtual_nodes_graph = []
    for i,j,cost in edgelist:
        v = (i,j)
        virtual_nodes_graph += [(i,v,cost), (v,j,0)]
    return virtual_nodes_graph

def virtual_node_edges():
    """
    仮想ノードを含むリンクを返す

    returns:
    * edges(edge list)
      仮想ノードを含むリンクを格納したリスト
    """
    global edgelist
    edges = []
    virtual_nodes_graph = []
    for i,j,cost in edgelist:
        v = (i,j)
        edges += [[(i,v)], [(v,j)]]
    return edges

def virtual_nodes():
    """
    仮想ノードのリストを返す

    returns:
    * virtual_nodes(nodes list)
      仮想ノードを格納したリスト
    """
    global edgelist
    v_nodes = []
    for i,j,cost in edgelist:
        v = (i,j)
        v_nodes.append(v)
    return v_nodes

def original_nodes():
    global edgelist
    edges = [[i,j] for i,j,cost in edgelist]
    return set(reduce(lambda x,y: x + y, edges))

def predecessor_nodes(node):
    """
    仮想ノード追加前のグラフのノードのリストを返す

    returns:
    * nodes(node set)
      仮想ノード追加前のグラフのノードを格納したリスト
    """
    """
    nodeへの流入リンク(predecessor, node)を構成するノードpredecessorを返す

    returns:
    * predecessors(node list)
      predecessorノードを格納したリスト
    """
    global edgelist
    v_nodes = virtual_nodes()
    predecessors = []
    for i,j in v_nodes:
        if node == j:
            predecessors.append((i,j))
    return predecessors

def internal_edges(node):
    """
    rule1

    arguments:
    * node(node label)

    returns:
    * internal_edges(list)
      rule1にあてはまるサブグラフからなるlist
    """
    predecessors = predecessor_nodes(node)
    il = [[(p, node)] for p in predecessors]
    return il

def two_internal_edges_subgraph(node):
    """
    rule2

    arguments:
    * node(node label)

    returns:
    * subgraphs(list)
      rule2にあてはまるサブグラフからなるlist
    """
    try:
        in_edges = [e[0] for e in internal_edges(node)]
        if len(in_edges) < 2:
            raise ValueError("Error Message")
    except ValueError:
        print "node {} has no two and over internal edges".format(node)
    else:
        subgraphs = [[e1, e2] for e1,e2 in combinations(in_edges, 2)]
        return subgraphs

def invalid_direction_elms(start_node, target_node):
    """
    rule1とrule2をまとめたグラフセット形式のリストを返す

    arguments:
    * start_node(node label)
    * target_node(node label)

    returns:
    * elms(list)
    rule1とrule2をまとめたグラフセット形式のリスト
    """
    rule1 = internal_edges(start_node)
    rule2_nodes = original_nodes() - {start_node, target_node}
    elms = [e for e in rule1]
    for node in rule2_nodes:
        try:
            rule2 = two_internal_edges_subgraph(node)
        except ValueError:
            continue
        else:
            for subgraph in rule2:
                elms.append(subgraph)
    return elms

def directed_paths(start_node, target_node):
    """
    有効性を考慮したパスだけを含むグラフセットを返す

    arguments:
    * start_node(node label)
    * target_node(node label)

    returns:
    * di_paths(GraphSet)
      有効性を考慮したパスだけを含むグラフセット
    """
    elms = invalid_direction_elms(start_node, target_node)
    elms = GraphSet(elms)
    di_paths = GraphSet.paths(start_node, target_node)
    di_paths = di_paths.excluding(elms)
    return di_paths

if __name__ == "__main__":
    # 動作確認
    edgelist = [(1,2,10),(1,3,20),(2,3,30),(2,4,40),(3,4,50),
                (2,1,-10),(3,1,-20),(3,2,-30),(4,2,-40),(4,3,-50)]
    read_edgelist(edgelist)
    print "append_virtual_nodes", append_virtual_nodes()
    print "virtual_node_edges", virtual_node_edges()
    print "virtual_nodes", virtual_nodes()
    print "predecessor_nodes", predecessor_nodes(4)
    print "internal_edges", internal_edges(1)
    print "two_internal_edges_subgraph", two_internal_edges_subgraph(1)
    print "directed_paths", directed_paths(1,4)
