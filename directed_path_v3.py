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
1. グラフの重み付きリンクのタプル(i,j,cost)を要素とするリストedgelistを用意する
2. GraphSet.set_universe(append_virtual_nodes(edgelist))を実行してGraphillionに仮想ノードを追加したグラフを読み込ませる
3. directed_paths(edgelist, start_node, target_node)を実行する
"""

from itertools import combinations
from collections import defaultdict
from math import log10

from graphillion import GraphSet

def same_nodes_link_dict(edgelist):
    """
    キーが(i,j)、値が[(i,j,cost1),(j,i,cost2)]の辞書を返す

    arguments:
    * edgelist(edge list)
      グラフを構成する重み付きの辺のタプルを要素とするリスト

    returns:
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
    * virtual_nodes_graph(edge list)
      仮想ノードを追加したグラフの重み付き辺のタプルを要素とするリスト
    """
    d = same_nodes_link_dict(edgelist)
    virtual_nodes_graph = []
    for link1,link2 in d.values():
        i, j, cost = link2[0], link2[1], link2[2]
        v = (i,j)
        virtual_nodes_graph += [link1, (i,v,cost), (v,j,0)]
    return virtual_nodes_graph

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
    * predecessors(node list)
      predecessorノードを格納したリスト
    """
    virtual_nodes = get_virtual_nodes(edgelist)
    predecessors = []
    for i,j in virtual_nodes:
        if node == i:
            predecessors.append(j)
        elif node == j:
            predecessors.append((i,j))
    return predecessors

def get_neighbor_nodes(edgelist, node):
    """
    nodeの流出リンク(node, neighbor)を構成するノードneighborを返す

    arguments:
    * edgelist(edge list)
    * node(node label)

    returns:
    * neighbors(node list)
      neighborノードを格納したリスト
    """
    neighbors = [list(l[0]) for l in external_links(edgelist, node)]
    neighbors = set(reduce(lambda x,y: x + y, neighbors)) - {node}
    return neighbors

def external_links(edgelist, node):
    """
    nodeの流出リンクを返す

    arguments:
    * edgelist(edge list)
    * node(node label)

    returns:
    * external_links(link)
      nodeの流出リンク
    """
    in_links = internal_links(edgelist, node)
    ex_links = [l for l in GraphSet({}).graph_size(1).including(node) - GraphSet(in_links)]
    return ex_links

def connected_links(edgelist, start_node, num_edges=2):
    """
    パス長がnum_edgesのパスを求める
    TODO: 2016.11.20
    * 任意のパス長を指定できるようにする
    * GraphSet.graphsを使う方法を検討
      * 仮想ノードを通ることによるパス長の変化にどうやって対応するか

    arguments:
    * edgelist(edge list)
    * start_node(node label)

    returns:
    * link_combinations(list)
      グラフセット形式で表されたパス長がnum_edgesのパスを格納したリスト
    """
    start_neighbors = get_neighbor_nodes(edgelist, start_node)
    done = {start_node}
    node_combinations = []
    for sn in start_neighbors:
        other_neighbors = list(get_neighbor_nodes(edgelist, sn) - done)
        for on in other_neighbors:
            if isinstance(on, tuple):
                if on[0] == start_node or on[1] == start_node:
                    other_neighbors.remove(on)
        node_combinations.append([[start_node, sn, n] for n in other_neighbors])
        done |= {sn}

    for c in node_combinations:
        for nodes in c:
            for node in nodes:
                if isinstance(node, tuple):
                    nodes.append(node[1])
    node_combinations = reduce(lambda x,y: x + y, node_combinations)
    link_combinations = []
    for c in node_combinations:
        temp = []
        for i in range(len(c) - 1):
            temp.append(tuple(c[i:i+2]))
        link_combinations.append(temp)
    return link_combinations

def internal_links(edgelist, node):
    """
    rule1

    arguments:
    * edgelist(edge list)
    * node(node label)

    returns:
    * internal_links(list)
      rule1にあてはまるサブグラフからなるlist
    """
    predecessors = get_predecessor_nodes(edgelist, node)
    il = [[(p, node)] for p in predecessors]
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
    di_paths = GraphSet.paths(start_node, target_node)
    di_paths = di_paths.excluding(elms)
    return di_paths

def total_cost(cost_dict, path):
    """
    パスの総コストを返す

    arguments:
    * cost_dict(dictionary)
      key: (i,j)
      value: cost
    * path(list)
      重み付き辺のタプル(i,j,cost)を要素とするリスト

    returns:
    * total_cost(int or float)
      pathを構成するリンクの重みの総和
    """
    return sum([cost_dict[e] for e in path])

def convert_common_logarithm(probabilities):
    """
    リンク利用確率pに対して常用対数を取る

    arguments:
    * probabilities(dictionary)
      key: (i,j)
      value: probability
    
    returns:
    * conv_prob(dictionary)
      key: (i,j)
      value: probabilityに対して常用対数を取った値
    """
    conv_prob = {}
    for link,prob in probabilities.items():
        conv_prob[link] = log10(prob)
    return conv_prob

def calc_probability(probabilities, path):
    """
    パスの利用確率を求める  
    各リンクの故障は独立に起こるとする

    利用確率の昇順・降順でパス列挙を行いたいのでmax_iter(),min_iter()との連携を考える
    これらのメソッドはパスの重みの総和の大小を扱う。一方、リンク利用可能性は独立な事象なので
    パスの利用確率は積で取る必要がある
    この積の計算を和の計算に直す
    例として、2つのリンク(i,j,0.9),(j,k,0.9)からなるパスの利用確率を求める
    1. 各リンクの利用確率に対して常用対数をとる
       log10(0.9) = -0.045757490560675115
    2. それらの値の総和をとる。これをexponentとおく
       log10(0.9) + log10(0.9) = -0.09151498112135023
    3. 10 ** exponentが利用確率である
       10 ** (log10(0.9) + log10(0.9)) = 0.81

    arguments:
    * probabilities(dictionary)
      key: (i,j)
      value: probabilityに対して常用対数を取った値
    * path
      重み付き辺のタプル(i,j,cost)を要素とするリスト

    returns:
    * probability(float)
      pathの利用確率
    """
    exponent = total_cost(probabilities, path)
    return 10 ** exponent

if __name__ == "__main__":
    # 動作確認
    edgelist = [(1,2,1),(1,3,2),(2,3,3),(2,4,4),(3,4,5),
                (2,1,-1),(3,1,-2),(3,2,-3),(4,2,-4),(4,3,-5)]
    prob = {(i,j): .99 for i,j,cost in append_virtual_nodes(edgelist)}
    conv_prob = convert_common_logarithm(prob)

    GraphSet.set_universe(append_virtual_nodes(edgelist))
    print "virtual_nodes", get_virtual_nodes(edgelist)
    print "predecessor_nodes", get_predecessor_nodes(edgelist, 1)
    print "neighbor_nodes", get_neighbor_nodes(edgelist, 1)
    print "internal_links", internal_links(edgelist, 1)
    print "external_links", external_links(edgelist, 1)
    print "two_internal_links_subgraph", two_internal_links_subgraph(edgelist, 1)
    print "connected_links", connected_links(edgelist, 2)
    paths_2_3 = directed_paths(edgelist, 2, 3)
    choiced = paths_2_3.choice()
    print choiced
    print conv_prob
    print calc_probability(conv_prob, choiced)
    for path in paths_2_3:
        print path
