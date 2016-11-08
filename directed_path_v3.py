# coding: utf-8

"""
author Mio Kinno
date 2016.11.7
branch master
file directed_path_v3.py

graphillion.Graphset.pathsメソッドが求めたパスからグラフの方向性を考慮したパスを取り出す


# 動作概要

## 仮想ノード
仮想ノードを追加し(i,j,cost1),(j,i,cost2)のような構成ノードは同じだが方向性が異なるリンクを
Graphillionで扱えるようにする
これまで2個追加していた仮想ノードをこのモジュールでは1個に減らした

仮想ノードの追加は以下のように行う

* リンク(i,j,cost1)に対して  
   仮想ノードを設けずにリンク(i,j,cost1)をそのまま使用する  

* リンク(j,i,cost2)に対して  
  仮想ノードj_iを設ける  
  リンク(j,j_i,cost2),(j_i,i,0)を追加する

## 不要なサブグラフの除外
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
2. GraphSet.set_universe(append_virtual_nodes(edgelist))を実行してGraphillionに仮想ノードを追加したグラフを読み込ませる
3. directed_paths(edgelist, start_node, target_node)を実行する

# 予定
* 仮想ノードを文字列からタプルに変更
* rule1,2の関数をgeneratorに変更   
"""

from itertools import combinations
from collections import defaultdict

from graphillion import GraphSet

def same_nodes_link_dict(edgelist):
    """
    キーが(i,j)、値が[(i,j,cost1),(j,i,cost2)]の辞書を返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    return:
    * d(defaultdict)
      key: (i,j)
      value: [(i,j,cost1),(j,i,cost2)]
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
    仮想ノードを追加したグラフの辺のリストを返す

    arguments:
    * edgelist(edge list)
    
    returns:
    * virtual_nodes_Graph(edge list)
      仮想ノードを追加したグラフの重み付き辺のタプルを要素とするリスト
    """
    d = same_nodes_link_dict(edgelist)
    virtual_nodes_Graph = []
    for link1,link2 in d.values():
        i, j, cost = link2[0], link2[1], link2[2]
        v = (i,j)
        virtual_nodes_Graph += [link1, (i,v,cost), (v,j,0)]
    return virtual_nodes_Graph

def get_virtual_nodes(edgelist):
    """
    仮想ノードのリストを返す

    arguments:
    * edgelist(edge list)

    returns:
    * virtual_nodes(nodes list)
      仮想ノードを格納したリスト
    """
    d = same_nodes_link_dict(edgelist)
    virtual_nodes = []
    for link1,link2 in d.values():
        i, j, cost = link2[0], link2[1], link2[2]
        virtual_nodes.append((i,j))
    return virtual_nodes

def get_original_nodes(edgelist):
    """
    仮想ノード追加前のグラフのノードのリストを返す

    arguments:
    * edgelist(edge list)

    returns:
    * nodes(node list)
      仮想ノード追加前のグラフのノードを格納したリスト
    """
    edges = [[i,j] for i,j,cost in edgelist]
    return set(reduce(lambda x,y: x + y, edges))

def get_predecessor_nodes(edgelist, node):
    """
    nodeへの流入リンク(predecessor, node)を構成するノードpredecessorを返す

    arguments:
    * edgelist(edge list)
    * node(node label)

    returns:
    * predecessor_nodes(node list)
      predecessorノードを格納したリスト
    """
    virtual_nodes = get_virtual_nodes(edgelist)
    predecessor_nodes = []
    for i,j in virtual_nodes:
        if node == i:
            predecessor_nodes.append(j)
        elif node == j:
            predecessor_nodes.append((i,j))
    return predecessor_nodes

def internal_links(edgelist, node):
    """
    rule1

    arguments:
    * edgelist(edge list)

    returns:
    * internal_links(list)
      rule1にあてはまるサブグラフからなるlist
    """
    predecrssors = get_predecessor_nodes(edgelist, node)
    il = [[(p, node)] for p in predecrssors]
    return il

def two_internal_links_subgraph(edgelist, node):
    """
    rule2

    arguments:
    * edgelist(edge list)

    returns:
    * subgraphs(list)
      rule2にあてはまるサブグラフからなるlist
    """
    il = [link[0] for link in internal_links(edgelist, node)]
    if len(il) < 2:
        return
    subgraphs = [[link1, link2] for link1,link2 in combinations(il, 2)]
    return subgraphs

def directed_paths(edgelist, start_node, target_node):
    """
    有効性を考慮したパスだけを含むグラフセットを返す

    arguments:
    * edgelist(edge list)
    * start_node(node label)
    * target_node(node label)

    returns:
    * di_paths(GraphSet)
      有効性を考慮したパスだけを含むグラフセット
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
    # edgelist = [(u"1",u"2",1),(u"1",u"3",2),(u"2",u"3",3),(u"2",u"4",4),(u"3",u"4",5),
    #             (u"2",u"1",-1),(u"3",u"1",-2),(u"3",u"2",-3),(u"4",u"2",-4),(u"4",u"3",-5)]
    edgelist = [(1,2,1),(1,3,2),(2,3,3),(2,4,4),(3,4,5),
                (2,1,-1),(3,1,-2),(3,2,-3),(4,2,-4),(4,3,-5)]

    GraphSet.set_universe(append_virtual_nodes(edgelist))
    print append_virtual_nodes(edgelist)
    print "virtual_nodes", get_virtual_nodes(edgelist)
    print "predecessor_nodes", get_predecessor_nodes(edgelist, 1)
    print "internal_links", internal_links(edgelist, 1)
    print "two_internal_links_subgraph", two_internal_links_subgraph(edgelist, 1)
    for path in directed_paths(edgelist, 2, 3):
        print path
