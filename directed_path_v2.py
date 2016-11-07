# coding: utf-8

"""
author Mio Kinno
date 2016.10.31
branch master
file directed_path_v2.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す

# 動作概要
branch two_virtual_nodes_NetworkXと動作は同じだが
NetworkXを一切使用しない実装
不要なサブグラフのグラフセットの作成をまとめて行うことで高速化

# 使い方
**ノードのラベルは必ずunicode文字列とすること**
1. グラフの重み付きリンクのタプル(i,j,cost)を要素とするリストedgelistを用意する
2. GraphSet.set_universe(append_virtual_nodes(edgelist))を実行してGraphillionに仮想ノードを追加したグラフを読み込ませる
3. directed_paths(edgelist, start_node, target_node)を実行する

"""

from itertools import combinations

from graphillion import GraphSet

def append_virtual_nodes(edgelist):
    """
    仮想ノードを追加したグラフの辺のリストを返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト
      ノードのラベルは必ず文字列とすること

    returns:
    * virtual_nodes_Graph(edge list)
      仮想ノードを追加した重み付きの辺のタプルを要素とするリスト
    """
    virtual_nodes_Graph = []
    for i,j,cost in edgelist:
        v = i + "_" + j
        virtual_nodes_Graph.append((i,v,cost))
        virtual_nodes_Graph.append((v,j,0))
    return virtual_nodes_Graph

def get_virtual_nodes(edgelist):
    """
    仮想ノードのリストを返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    returns:
    * virtual_nodes(node list)
      仮想ノードを要素とするリスト
    """
    virtual_nodes = []
    for i,j,cost in edgelist:
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

def get_internal_nodes(edgelist, node):
    """
    nodeへの流入リンクを構成するノードのリストを返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト
      ノードのラベルは必ず文字列とすること
    * node(node label)
    
    returns:
    * nodes(node list)
      nodeへの流入リンクを構成するノードのリスト
    """
    virtual_nodes = get_virtual_nodes(edgelist)
    nodes = []
    for v in virtual_nodes:
        i, j = v.split(("_"))
        if node == j:
            nodes.append(v)
    return nodes

def internal_links(edgelist, node):
    """
    rule1

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    returns:
    * internal_links(GraphSet)
      rule1にあてはまるサブグラフからなるGraphSet
    """
    nodes = get_internal_nodes(edgelist, node)
    il = [[(v,node)] for v in nodes]
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
    rule1とrul2にあてはまる要素をまとめたリストを返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト
    * start_node(node label)
    * target_node(node label)

    returns:
    * elms(list)
      rule1とrule2にあてはまる除外すべきグラフの要素を格納したリスト
    """
    rule1 = internal_links(edgelist, start_node)
    rule2_nodes = get_original_nodes(edgelist) - {start_node, target_node}
    elms = []
    for link in rule1:
        elms.append(link)
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
    # print "virtual_nodes_Graph", append_virtual_nodes(edgelist)
    # print internal_links(edgelist, u"1")
    # print two_internal_links_subgraph(edgelist, u"3")
    for path in directed_paths(edgelist, u"1", u"2"):
        print path
