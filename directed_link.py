"""
author Mio Kinno
date 2017.6.21
branch master
file directed_link.py

仮想ノードを追加し(i,j,cost1),(j,i,cost2)のような構成ノードは同じだが方向性が異なるリンクを
Graphillionで扱えるようにする
これまで2個追加していた仮想ノードをこのモジュールでは1個に減らした


# 動作概要

## 仮想ノード

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
1. グラフの重み付きリンクのタプル(i,j,cost)を要素とするリストedgelistを用意する。
2. read_edgelist(edgelist)を実行してモジュールにedgelistを読み込ませる
3. GraphSet.set_universe(append_virtual_nodes())を実行してGraphillionに仮想ノードを追加したグラフを読み込ませる
4. directed_paths(start_node, target_node)を実行する
"""

from itertools import combinations
from functools import reduce
from collections import defaultdict
import math
import random

from graphillion import GraphSet

VIRTUAL_NODE_DIGIT_I = 1000
VIRTUAL_NODE_DIGIT_J = 100

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

def virtual_node_expression(i, j):
    """
    リンク(j,i)間の仮想ノードを返す
    QQQ 2017.8.29
    いまのところこの式を使う

    arguments:
    * i(node label)
    * j(node label)

    returns:
    * v_node(node label)
      リンク(j,i)間の仮想ノード
    """
    return i * VIRTUAL_NODE_DIGIT_I + j * VIRTUAL_NODE_DIGIT_J

def devide_virtual_node(v_node):
    """
    仮想ノードをノードi,jに分割する

    arguments:
    * v_node(virtual node label)

    returns:
    * (i,j)(tuple)
    """
    i, j = divmod(v_node, VIRTUAL_NODE_DIGIT_I)
    j = j // VIRTUAL_NODE_DIGIT_J
    return (i, j)

def virtual_node_iter():
    """
    仮想ノードを返すジェネレータ

    yields:
    * (i, j, cost)(tuple)
      i,jはvirtual_node_expressionで使用するノードラベル
      costは仮想ノードを設けることで発生するリンクに付与する重み
    """
    d = edges_table()
    for e1,e2 in d.values():
        i, j, cost = e2[0], e2[1], e2[2]
        yield (i, j, cost)

def append_virtual_nodes():
    """
    仮想ノードを追加したグラフの辺のリストを返す

    returns:
    * virtual_nodes_graph(edge list)
      仮想ノードを追加したグラフの重み付き辺のタプルを要素とするリスト
    """
    d = edges_table()
    virtual_nodes_graph = []
    for e1,e2 in d.values():
        i, j, cost = e2[0], e2[1], e2[2]
        v = virtual_node_expression(i, j)
        virtual_nodes_graph += [e1, (i, v, cost), (v, j, 0)]
    return virtual_nodes_graph

def append_virtual_nodes2():
    """
    仮想ノードの追加を別のルールで行う

    * リンク(i,j,cost1)に対して
      仮想ノードi_jを設ける
      リンク(i,i_j,cost2),(i_j,j,0)を追加する

    * リンク(j,i,cost2)に対して
      仮想ノードを設けずにリンク(j,i,cost2)をそのまま使用する
    """
    d = edges_table()
    virtual_nodes_graph = []
    for e1,e2 in d.values():
        i, j, cost = e1[0], e1[1], e1[2]
        v = virtual_node_expression(i, j)
        virtual_nodes_graph += [(i, v, cost), (v, j, 0), e2]
    return virtual_nodes_graph

def virtual_node_edges():
    """
    仮想ノードを含むリンクを返す

    returns:
    * edges(edge list)
      仮想ノードを含むリンクを格納したリスト
    """
    edges = []
    for i,j,cost in virtual_node_iter():
        v = virtual_node_expression(i, j)
        edges += [[(i, v)], [(v, j)]]
    return edges

def virtual_node_table():
    """
    キーがリンク(i,j)，値が(i,j)間の仮想ノードである辞書を返す

    returns:
    * v_table(dict)
    """
    v_table = {}
    edges = []
    for i,j,cost in virtual_node_iter():
        v = virtual_node_expression(i, j)
        v_table[(i,j)] = v
    return v_table

def virtual_nodes():
    """
    仮想ノードのリストを返す

    returns:
    * virtual_nodes(nodes list)
      仮想ノードを格納したリスト
    """
    v_nodes = []
    for i,j,cost in virtual_node_iter():
        v_nodes.append(virtual_node_expression(i, j))
    return v_nodes

def original_nodes():
    """
    仮想ノード追加前のグラフのノードのリストを返す

    returns:
    * nodes(node set)
      仮想ノード追加前のグラフのノードを格納したリスト
    """
    global edgelist
    edges = [[i,j] for i,j,cost in edgelist]
    return list(set(reduce(lambda x,y: x + y, edges)))

def predecessor_nodes(node):
    """
    nodeへの流入リンク(predecessor, node)を構成するノードpredecessorを返す

    returns:
    * predecessors(node list)
      predecessorノードを格納したリスト
    """
    global edgelist
    v_nodes = virtual_nodes()
    v_table = virtual_node_table()
    predecessors = []
    for i,j in v_table.keys():
        if node == i:
            predecessors.append(j)
        elif node == j:
            predecessors.append(virtual_node_expression(i, j))
    return predecessors

def neighbor_nodes(node):
    """
    nodeの流出リンク(node, neighbor)を構成するノードneighborを返す

    arguments:
    * node(node label)

    returns:
    * neighbors(node list)
      neighborノードを格納したリスト
    """
    global edgelist
    neighbors = [list(l[0]) for l in external_edges(node)]
    neighbors = list(set(reduce(lambda x,y: x + y, neighbors)) - {node})
    return neighbors

def external_edges(node):
    """
    nodeの流出リンクを返す

    arguments:
    * node(node label)

    returns:
    * external_edges(list)
      nodeの流出リンク
    """
    in_edges = internal_edges(node)
    ex_edges = [l for l in GraphSet({}).graph_size(1).including(node) - GraphSet(in_edges)]
    return ex_edges

def original_path(path):
    """
    仮想ノードを追加したグラフから求めたパスを元のグラフのパスに変換する

    arguments:
    * path(list)
      辺を表すタプル(i,j)を要素とするリスト

    returns:
    * o_path(list)
      pathから仮想ノードを除去した元のグラフのパス
    """
    _path = path[:]
    o_path = []
    v_table = virtual_node_table()
    v_table_inv = {v:k for k,v in v_table.items()}
    v_nodes = virtual_nodes()
    for i,j in _path:
        if i in v_nodes:
            o_edge = v_table_inv[i]
            o_path.append(v_table_inv[i])
            _path.remove((o_edge[0], i))
        elif j in v_nodes:
            o_edge = v_table_inv[j]
            o_path.append(v_table_inv[j])
            _path.remove((j, o_edge[1]))
        else:
            o_path.append((i,j))
    return o_path

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
        print("node {} has no two and over internal edges".format(node))
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
    rule2_nodes = set(original_nodes()) - {start_node, target_node}
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
    有向性を考慮したパスだけを含むグラフセットを返す

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

def connected_edges(start_node, target_node, num_edges):
    """
    start_nodeをパスのスタートノードとし、かつtarget_nodeを含まない
    長さがnum_edgesのパスを含むグラフセットを返す
    パスが仮想ノードを２個以上通るときnum_edgesよりも短いパスもグラフセットに含まれてしまう

    arguments:
    * start_node(node label)
    * target_node(node label)
    * num_edges(int)
      パスの長さ

    returns:
    * di_path(GraphSet)
      有向性を考慮したパスだけを含むグラフセット
    """
    all_nodes = set(original_nodes()) | set(virtual_nodes())
    v_nodes = virtual_nodes()
    degree_constraints = {}
    for node in all_nodes:
        if node in v_nodes:
            degree_constraints[node] = [0, 2]
        elif node == start_node:
            degree_constraints[node] = 1
        elif node == target_node:
            degree_constraints[node] = 0
        else:
            degree_constraints[node] = [0, 1, 2]

    elms = invalid_direction_elms(start_node, target_node)
    v_edges = virtual_node_edges()
    n_range = GraphSet.graphs(vertex_groups=[[start_node]],
                              no_loop=True,
                              num_edges=num_edges,
                              degree_constraints=degree_constraints)
    n_inc_range = GraphSet.graphs(vertex_groups=[[start_node]],
                                  no_loop=True,
                                  num_edges=num_edges+1,
                                  degree_constraints=degree_constraints)
    n_range = n_range.excluding(GraphSet(elms))\
                     .excluding(GraphSet(v_edges))
    n_inc_range = n_inc_range.excluding(GraphSet(elms))\
                             .including(GraphSet(v_edges))
    return n_range | n_inc_range

def disjoint_paths(paths, path):
    """
    パスのグラフセットから指定したパスのlink-disjoint pathを求める

    arguments:
    * paths(GraphSet)
    * path(list)

    returns:
    * di_paths(GraphSet)
    """
    disjoint_elms = [[e] for e in path]
    return paths.excluding(GraphSet(disjoint_elms))

def bidirectional_disjoint_paths(paths, path):
    """
    パスのグラフセットから指定したパスの双方向link-disjoint pathを求める
    双方向にリンクが共有されないようにする
    つまり(i,j), (j,v), (v,i)と共有されないパス集合が返る

    arguments:
    * paths(GraphSet)
    * path(list)

    returns:
    * di_paths(GraphSet)
    """
    disjoint_elms = []
    v_nodes = virtual_nodes()
    v_table = virtual_node_table()
    for e in path:
        if e[0] in v_nodes:
            i, j = v_table[e[0]]
            disjoint_elms += [[(i,j)], [(e[0],i)], [(j,e[0])]]
        elif e[1] in v_nodes:
            j, i = v_table[e[1]]
            disjoint_elms += [[(i,j)], [(e[1],i)], [(j,e[1])]]
        else:
            disjoint_elms.append([e])
            i, j = e[0], e[1]
            v = virtual_node_expression(i, j)
            if v in v_nodes:
                disjoint_elms += [[(i,v)], [(v,j)]]
            else:
                v = virtual_node_expression(j, i)
                disjoint_elms += [[(i,v)], [(v,j)]]
    return paths.excluding(GraphSet(disjoint_elms))

def total_cost(cost_dict, path):
    """
    重み付き辺の重みの和を返す

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

def probability_dict(pmin=None, pmax=None):
    """
    グラフの各辺にリンク利用確率を設定する

    arguments:
    * pmin(float)
      利用確率の下限
    * pmax(float)
      利用確率の上限

    returns:
    * prob(dict)
      key: (i,j)
      value: probability
    """
    if pmin is None:
        pmin = .9
    if pmax is None:
        pmax = .99

    prob = {}
    d = edges_table()
    for e1,e2 in d.values():
        i, j = e2[0], e2[1]
        v = (i, j)
        r = random.uniform(pmin, pmax)
        prob[(e1[0], e1[1])] = r
        prob[(i, v)] = r
        prob[(v, j)] = 1

    return prob

def convert_common_logarithm(probabilities):
    """
    リンク利用確率に対して常用対数を取る

    arguments:
    * probabilities(dictionary)
      key: (i,j)
      value: probability

    returns:
    * conv_prob(dictionary)
      key: (i,j)
      value: probabilityに対して常用対数を取った値
    """
    conv_prob = {link: math.log10(prob) for link,prob in probabilities.items()}
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
    conv_prob = convert_common_logarithm(probabilities)
    exponent = total_cost(conv_prob, path)
    return 10 ** exponent

if __name__ == "__main__":
    # 動作確認
    edgelist = [(1,2,10),(1,3,20),(2,3,30),(2,4,40),(3,4,50),
                (2,1,10),(3,1,20),(3,2,30),(4,2,40),(4,3,50)]

    read_edgelist(edgelist)
    GraphSet.set_universe(append_virtual_nodes())

    print("edges_table", edges_table())
    print("append_virtual_nodes", append_virtual_nodes())
    print("append_virtual_nodes2", append_virtual_nodes2())
    print("universe", GraphSet.universe())
    print("virtual_node_edges", virtual_node_edges())
    print("virtual_nodes", virtual_nodes())
    print("original_nodes", original_nodes())
    print("predecessor_nodes", predecessor_nodes(1))
    print("internal_edges", internal_edges(2100))
    print("neighbor_nodes", neighbor_nodes(1))
    print("external_edges", external_edges(4))
    print("two_internal_edges_subgraph", two_internal_edges_subgraph(2100))
    print("invalid_direction_elms", invalid_direction_elms(4, 3))
    di_paths_1_4 = directed_paths(1, 4)
    print("directed_paths", di_paths_1_4)
    for path in di_paths_1_4:
        print(path)
    print("connected_edges", connected_edges(1, 4, 2))
    print("disjoint_paths", disjoint_paths(di_paths_1_4, [(3,3200), (3200,2)]))
    print("bidirectional_disjoint_paths", bidirectional_disjoint_paths(di_paths_1_4, [(4,4300), (4300,3), (3,3100), (3100,1)]))
    print("original_path", original_path([(4, 4300), (4300, 3), (3, 3100), (3100, 1)]))
    print("probability_dict", probability_dict())
