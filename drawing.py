# coding: utf-8

"""
author Mio Kinno
date 2016.11.11
branch master
file drawing.py

モデルデータcost239,jpn,nsfnet,akitaを描画する
figsizeは以下の値を指定すると見やすい
cost239 (9, 6)
jpn (18, 15)
nsfnet (15, 9)or(6, 9)
akita (15, 18)or(12, 15)or(6, 9)
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from dat_utils import Dat

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
    path = "../model_data_coordinates/"
    data = {"cost239": path + "cost239_coordinates_fixed.csv",
            "jpn12":   path + "jpn12_coordinates.csv",
            "jpn25":   path + "jpn25_coordinates.csv",
            "jpn48":   path + "jpn48_coordinates.csv",
            "nsfnet":  path + "NSFNET_coordinates.csv",
            "akita":   path + "akita_cities_coordinates.csv"}
    csv = pd.read_csv(data[model])
    coordinates = zip(csv["longitude"], csv["latitude"])
    pos = {city: coordinate for city,coordinate in zip(csv["index"], coordinates)}
    return pos

def model_data_graph(model):
    """
    モデルデータのグラフを作成する

    arguments:
    * model(string)

    returns:
    * G(networkx Graph object)
    """
    path = "../model_data/"
    data = {"cost239": path + "COST239/cost239_EQ_200.dat",
            "jpn12":   path + "JPNM/JPN12/JPN12_EQ_200.dat",
            "jpn25":   path + "JPNM/JPN25/JPN25_EQ_200.dat",
            "jpn48":   path + "JPNM/JPN48/JPN48_EQ_200.dat",
            "nsfnet":  path + "NSFNET/nsfnet_EQ_200.dat",
            "akita":   path + "Akita/akita_TE.dat"}
    model_data = Dat(data[model])
    edges = model_data.read_params("cost", lambda p: (int(p[0]), int(p[1])))
    G = nx.Graph(data=edges)
    return G

def draw_model_data(model, path=None, figsize=None):
    """
    モデルデータを描画する

    arguments:
    * model(string)
    * path(list optional)
      辺を表すタプルを要素とするリスト
      pathを指定するとpathに含まれるノードと辺が赤く描画される
    * figsize(tuple optional)
      描画する図の大きさ
      (width, height)の形式
    """
    pos = get_node_pos(model)
    G = model_data_graph(model)
    node_label = {node: node for node in G.nodes()}
    if figsize is not None:
        plt.figure(figsize=figsize)
    nx.draw_networkx_nodes(G, pos, node_color="w")
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos)
    if path is not None:
        nx.draw_networkx_nodes(nx.Graph(data=path), pos, node_color="r")
        nx.draw_networkx_labels(nx.Graph(data=path), pos, font_size=10, labels=node_label)
        nx.draw_networkx_edges(nx.Graph(data=path), pos, edgelist=path,
                               edge_color="r", width=3.0)
    plt.xticks([])
    plt.yticks([])
    plt.show()

if __name__ == '__main__':
    # 動作確認
    # cost239 = Dat("../model_data/COST239/cost239_EQ_200.dat")
    # cost239_edges = cost239.read_params("cost", lambda p: (int(p[0]), int(p[1])))
    # G1 = nx.Graph(data=list(cost239_edges))
    # G = model_data_graph("akita")
    # print(G.edges(), G.nodes())
    draw_model_data("jpn25", figsize=(12, 9), path=[(0,1),(1,2)])
    draw_model_data("cost239", figsize=(9, 6), path=[(0,1),(1,2)])
