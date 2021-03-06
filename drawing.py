# coding: utf-8

"""
author Mio Kinno
date 2016.11.11
branch master
file drawing.py

モデルデータcost239,jpn,nsfnet,akitaを描画する

このモジュールを取り込んだファイルからmodel_data_coordinatesとmodel_dataへの
適切な相対パスを設定すること

figsizeは以下の値を指定すると見やすい
cost239 (9, 6)
jpn (18, 15)
nsfnet (15, 9)or(6, 9)
akita (15, 18)or(12, 15)or(6, 9)
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from proposal_packages.dat_utils import Dat

# パスのデフォルト値
coordinate_path = "../model_data_coordinates/"
model_path = "../model_data/"

def set_default_coordinate_path(path=None):
    """
    model_data_coordinatesへのパスを設定する

    arguments:
    * path(string, optional)
      model_data_coordinatesへのパス
    """
    global coordinate_path
    if path is None:
        coordinate_path = "../model_data_coordinates/"
    else:
        coordinate_path = path

def set_default_model_path(path=None):
    """
    model_dataへのパスを設定する

    arguments:
    * path(string, optional)
      model_dataへのパス
    """
    global model_path
    if path is None:
        model_path = "../model_data/"
    else:
        model_path = path

def get_node_pos(model):
    """
    モデルデータの各ノードの座標を求める

    arguments:
    * model(string)
      モデルデータの名前。以下のいずれかを指定する
      cost239,jpn12or25or48,nsfnet,akita

    returns:
    * pos(dictionary)
      key: node label
      value: node position
    """
    global coordinate_path
    data = {"cost239": coordinate_path + "cost239_coordinates_fixed.csv",
            "jpn12":   coordinate_path + "jpn12_coordinates.csv",
            "jpn25":   coordinate_path + "jpn25_coordinates.csv",
            "jpn48":   coordinate_path + "jpn48_coordinates.csv",
            "nsfnet":  coordinate_path + "NSFNET_coordinates.csv",
            "akita":   coordinate_path + "akita_cities_coordinates.csv"}
    pos = create_node_pos_from_coordinate_csv(data[model])
    return pos

def model_data_graph(model):
    """
    モデルデータのグラフを作成する

    arguments:
    * model(string)

    returns:
    * G(networkx Graph object)
    """
    global model_path
    data = {"cost239": model_path + "COST239/cost239_EQ_200.dat",
            "jpn12":   model_path + "JPNM/JPN12/JPN12_EQ_200.dat",
            "jpn25":   model_path + "JPNM/JPN25/JPN25_EQ_200.dat",
            "jpn48":   model_path + "JPNM/JPN48/JPN48_EQ_200.dat",
            "nsfnet":  model_path + "NSFNET/nsfnet_EQ_200.dat",
            "akita":   model_path + "Akita/akita_TE.dat"}
    G = create_graph_from_dat(data[model])
    return G

def create_node_pos_from_coordinate_csv(coordinate_csv):
    data = pd.read_csv(coordinate_csv)
    coordinates = zip(data["longitude"], data["latitude"])
    pos = {index: coordinate for index, coordinate in zip(data["index"], coordinates)}
    return pos

def create_graph_from_dat(dat):
    model_data = Dat(dat)
    edges = model_data.read_params("cost", lambda p: (int(p[0]), int(p[1])))
    G = nx.Graph(data=edges)
    return G

def draw_graph(G, pos, subgraph=None, figsize=None, figname=None, jupyterinline=False):
    """
    グラフを描画する
    """
    node_label = {node: node for node in G.nodes()}
    if figsize is not None:
        plt.figure(figsize=figsize)
    nx.draw_networkx_nodes(G, pos, node_color="w")
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos)
    if subgraph is not None:
        nx.draw_networkx_nodes(nx.Graph(data=subgraph), pos, node_color="r")
        nx.draw_networkx_labels(nx.Graph(data=subgraph), pos, font_size=10, labels=node_label)
        nx.draw_networkx_edges(nx.Graph(data=subgraph), pos, edgelist=subgraph,
                               edge_color="r", width=3.0)
    plt.xticks([])
    plt.yticks([])

    if figname is not None:
        plt.savefig("./{}.png".format(figname), dpi=400, bbox_inches="tight", transparent=True)

    if not jupyterinline:
        plt.show()

def draw_model_data(model, subgraph=None, figsize=None, figname=False, jupyterinline=False):
    """
    モデルデータを描画する

    arguments:
    * model(string)
    * subgraph(edge list optional)
      部分グラフを表す辺を要素とするリスト
      subgraphを指定するとsubgraphに含まれるノードと辺が赤く描画される
    * figsize(tuple optional)
      描画する図の大きさ
      (width, height)の形式
    """
    pos = get_node_pos(model)
    G = model_data_graph(model)
    draw_graph(pos, G, subgraph, figsize, figname, jupyterinline)

if __name__ == '__main__':
    # 動作確認
    # cost239 = Dat("../model_data/COST239/cost239_EQ_200.dat")
    # cost239_edges = cost239.read_params("cost", lambda p: (int(p[0]), int(p[1])))
    # G1 = nx.Graph(data=list(cost239_edges))
    # G = model_data_graph("akita")
    # print(G.edges(), G.nodes())
    draw_model_data("jpn25", figsize=(12, 9), subgraph=[(0,1),(1,2)])
    draw_model_data("cost239", figsize=(9, 6), subgraph=[(0,1),(1,2)])
