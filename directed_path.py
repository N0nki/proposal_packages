# coding: utf-8

"""
author Mio Kinno
date 2016.10.26
file directed_path_v4.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す


# 動作概要
仮想ノードを追加し(i,j,cost1),(j,i,cost2)のような構成ノードは同じだが方向性が異なるリンクを
Graphillionで扱えるようにする
仮想ノードの追加は以下のように行う

* リンク(i,j,cost1)に対して  
  仮想ノードi_jを設ける  
  リンク(i,i_j,cost1),(i_j,j,0)を追加する

* リンク(j,i,cost2)に対して  
  仮想ノードj_iを設ける  
  リンク(j,j_i,cost2),(j_i,i,0)を追加する

仮想ノードを追加するだけでは方向性を考慮したパス列挙を行うことはできない
方向性を考慮したとき不要となるグラフの要素を除外する
除外のルールは以下の通り

* rule1
  スタートノードへの流入リンクをすべて除外

* rule2
  スタートノード、ターゲットノード以外のノードで流入リンクの次数が2以上のノードについて、
  そのノードの流入リンク2本からなるサブグラフをすべて除外
  あるノードの流入リンクの本数をnとすると除外するサブグラフはnC2個存在する

# 使い方
**ノードのラベルは必ずunicode文字列とすること**
1. グラフの重み付きリンクのタプル(i,j,cost)を要素とするリストedgelistを用意する
2. edgelistを引数としてappend_virtual_nodesを使用し、仮想ノードを追加したグラフの重み付きリンクを要素とするリストvgを得る
3. そのリストからNetwrokXの有向グラフオブジェクトを作成する(VG=nx.DiGraph();VG.add_weighted_edges_from(vg))
4. VG、スタートノード、ターゲットノードを引数としてdirected_pathsを実行

# 予定
仮想ノードの選択にNetworkXを使用しない方法を考える
（v4_1にて完成）
"""

from itertools import combinations

from graphillion import GraphSet
import networkx as nx

def append_virtual_nodes(Graph):
    """
    仮想ノードを追加したグラフの辺のリストを返す

    arguments:
    * Graph(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト
      ノードのラベルは必ず文字列とすること

    returns:
    * virtual_nodes_Graph(edge list)
      仮想ノードを追加した重み付きの辺のタプルを要素とするリスト
    """
    virtual_nodes_Graph = []
    for i,j,cost in Graph:
        v = i + "_" + j
        virtual_nodes_Graph.append((i,v,cost))
        virtual_nodes_Graph.append((v,j,0))
    return virtual_nodes_Graph

def get_virtual_nodes(Graph):
    """
    仮想ノードのリストを返す

    arguments:
    * Graph(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト
      ノードのラベルは必ず文字列とすること

    returns:
    * virtual_nodes(node list)
      仮想ノードを要素とするリスト
    """
    virtual_nodes = []
    for i,j,cost in Graph:
        v = i + "_" + j
        virtual_nodes.append(v)
    return virtual_nodes

def internal_links(DiGraph, node):
    """
    rule1

    arguments:
    * DiGraph(networkx directed Graph object)
    * node(node label)

    returns:
    * internal_links(list)
      rule1にあてはまるリンクからなるサブグラフを格納したリスト
    """
    il = [[(predecessor, node)]\
                      for predecessor in DiGraph.predecessors_iter(node)]
    return il
    
def two_internal_links_subgraph(DiGraph, node):
    """
    rule2

    arguments:
    * DiGraph(networkx directed Graph object)
    * node(node label)

    returns:
    * subgraphs(list)
      rule2にあてはまるサブグラフを格納したリスト
    """
    il = [link[0] for link in internal_links(DiGraph, node)]
    if len(il) < 2:
        return
    subgraphs = [[link1, link2] for link1,link2 in combinations(il, 2)]
    return subgraphs

def collect_invalid_direction_elms(DiGraph, start_node, target_node):
    """
    rule1とrul2にあてはまる要素をまとめたリストを返す

    arguments:
    * DiGraph(networkx directed Graph object)
    * start_node(node label)
    * target_node(node label)

    returns:
    * elms(list)
      rule1とrule2にあてはまる除外すべきグラフの要素を格納したリスト
    """
    rule1 = internal_links(DiGraph, start_node)
    # edgelist = [(i,j,attr['weight']) for i,j,attr in DiGraph.edges(data=True)]
    # virtual_nodes = get_virtual_nodes(edgelist)
    # rule2_nodes = set(DiGraph.nodes()) - set(virtual_nodes) - {start_node, target_node}
    # print "virtual_nodes", virtual_nodes
    # print "rule2 ndoes", rule2_nodes
    rule2_nodes = set(DiGraph.nodes()) - set((start_node, target_node))
    elms = []
    for path in rule1:
        elms.append(path)
    for node in rule2_nodes:
        rule2 = two_internal_links_subgraph(DiGraph, node)
        if rule2 is None: continue
        for subgraph in rule2:
            elms.append(subgraph)
    return elms

def directed_paths(DiGraph, start_node, target_node):
    """
    有効性を考慮したパスだけを含むグラフセットを返す

    arguments:
    * DiGraph(networkx directed Graph object)
    * start_node(start node label)
    * target_node(target node label)

    returns:
    * di_paths(GraphSet)
      有効性を考慮したパスだけを含むグラフセット
    """
    di_paths = GraphSet.paths(start_node, target_node)
    invalid_direction_elms = collect_invalid_direction_elms(DiGraph, start_node, target_node)
    gs = GraphSet(invalid_direction_elms)
    di_paths = di_paths.excluding(gs)
    return di_paths

if __name__ == "__main__":
    # 動作確認
    edgelist = [(u"1",u"2",1),(u"1",u"3",2),(u"2",u"3",3),(u"2",u"4",4),(u"3",u"4",5),
                (u"2",u"1",-1),(u"3",u"1",-2),(u"3",u"2",-3),(u"4",u"2",-4),(u"4",u"3",-5)]
    v = get_virtual_nodes(edgelist)
    vg = append_virtual_nodes(edgelist)
    DiG = nx.DiGraph()
    DiG.add_weighted_edges_from(vg)
    GraphSet.set_universe(DiG.edges())
    for i,path in enumerate(directed_paths(DiG, u"1", u"2")):
        print i, path

