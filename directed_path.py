# coding: utf-8

"""
author Mio Kinno
date 2016.10.31
branch master
file directed_path.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す

# 動作概要
branch two_virtual_nodes_NetworkXと動作は同じだが
NerworkXを一切使用しない実装
ループのなかでグラフセットを生成する処理が多いため非常に遅い
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
    # func = lambda v: v.split("_")
    # nodes = [i+"_"+j for i,j in map(func, virtual_nodes) if node == j]
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
    return GraphSet(il)

def two_internal_links_subgraph(edgelist, node):
    """
    rule2

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    returns:
    * subgraphs(GraphSet)
      rule2にあてはまるサブグラフからなるGraphSet
    """
    nodes = get_internal_nodes(edgelist, node)
    if len(nodes) < 2:
        return
    connected_nodes = [[node, v1, v2] for v1,v2 in combinations(nodes, 2)]
    subgraphs = GraphSet()
    for components in connected_nodes:
        subgraphs = subgraphs | GraphSet({}).graph_size(2).connected_components(components)
    return subgraphs

def directed_paths(edgelist, start_node, target_node):
    """
    有効性を考慮したパスだけを含むグラフセットを返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    returns:
    * di_paths(GraphSet)
      有効性を考慮したパスだけを含むグラフセット
    """
    rule1 = internal_links(edgelist, start_node)
    rule2_nodes = get_original_nodes(edgelist) - {start_node, target_node}
    rule2 = GraphSet()
    for node in rule2_nodes:
        subgraphs = two_internal_links_subgraph(edgelist, node)
        if subgraphs is None: continue
        rule2 = rule2 | subgraphs
    all_elms = rule1 | rule2

    di_paths = GraphSet.paths(start_node, target_node).excluding(all_elms)
    return di_paths

if __name__ == "__main__":
    # 動作確認
    edgelist = [(u"1",u"2",1),(u"1",u"3",2),(u"2",u"3",3),(u"2",u"4",4),(u"3",u"4",5),
                (u"2",u"1",-1),(u"3",u"1",-2),(u"3",u"2",-3),(u"4",u"2",-4),(u"4",u"3",-5)]
    v = get_virtual_nodes(edgelist)
    vg = append_virtual_nodes(edgelist)
    GraphSet.set_universe(vg)
    # print "original nodes", get_original_nodes(edgelist)
    # print "virtual_nodes", get_virtual_nodes(edgelist)
    # print "internal nodes", get_internal_nodes(edgelist, u"2")
    # print "internal links", internal_links(edgelist, u"3")
    # print "subgraphs", two_internal_links_subgraph(edgelist, u"1")
    for path in directed_paths(edgelist, u"1", u"2"):
        print path
