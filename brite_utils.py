"""
author mio kinno
date 2017.10.26
file brite_conv_utils.py
"""

from itertools import permutations

import pandas as pd
from pandas import DataFrame

class BRITEParser:
    """
    .briteファイルからノード，リンク，ネットワークの位置情報を取り出す．
    取り出された各データのフォーマットは以下のとおり
    * nodes
      ノードラベルを要素とするリスト
      e.g. ["0", "1", "2"]
    * edges
      各リンク情報を格納したリストを要素とするリスト
      e.g. [[node_i, node_j, cost, capacity]]
    * coordinates
      各ノードのx,y座標を格納した辞書．pandasのDataFrameで読み込める形式
      e.g. [{"node": "0", "x": 100, "y": 200}]

    参考
    BRITE/bin/brite2ns.py
    """

    def __init__(self, britefile):
        f = open(britefile)
        try:
            self.all_lines = f.read()
        finally:
            f.close()
        self.nodes = []
        self.edges = []
        self.coordinates = []
        self._parse()

    def _parse(self):
        state = 0
        for line in self.all_lines.splitlines():
            splited = line.split()
            if len(splited) == 0 or splited[0][0] == "#":
                continue
            if state == 0:
                if splited[0] == "Nodes:":
                    state = 1
            elif state == 1:
                if splited[0] == "Edges:":
                    state = 2
                else:
                    self.nodes.append(splited[0])
                    self.coordinates.append({"index": splited[0], "latitude": splited[1], "longitude": splited[2]})
            elif state == 2:
                self.edges.append([splited[1], splited[2], splited[4], splited[5]])

def to_dat(britefile, output):
    """
    BRITEParserが提供するデータフォーマットからdatファイルを生成する
    """
    brite = BRITEParser(britefile)
    nodes = brite.nodes
    edges = brite.edges
    traffic = list(permutations(nodes, 2))

    datfile = open(output, "w+")
    datfile.write("/* {} */\n\n".format(output))
    # dk, m, n
    datfile.write("param dk:=1\n")
    datfile.write("param m:={}\n".format(len(traffic)-1))
    datfile.write("param n:={}\n".format(len(nodes)-1))

    # HOP
    datfile.write("\n/* HOP */\n")
    datfile.write("param : EN :HOP:=\n")
    for edge in edges:
        datfile.write("{} {} 1\n".format(edge[0], edge[1]))
        datfile.write("{} {} 1\n".format(edge[1], edge[0]))
    datfile.write(";\n")

    # COST
    datfile.write("\n/* cost metric:delay */\n")
    datfile.write("param : EM :COST:=\n")
    for edge in edges:
        datfile.write("{} {} {}\n".format(edge[0], edge[1], edge[2]))
        datfile.write("{} {} {}\n".format(edge[1], edge[0], edge[2]))
    datfile.write(";\n")

    # Capacity
    datfile.write("\n/* link capacity:bandwidth */\n")
    datfile.write("param : E :C:=\n")
    for edge in edges:
        datfile.write("{} {} {}\n".format(edge[0], edge[1], edge[3]))
        datfile.write("{} {} {}\n".format(edge[1], edge[0], edge[3]))
    datfile.write(";\n")

    # traffic start node
    datfile.write("\n/* traffic matrix:start node */\n")
    datfile.write("param : SK :s:=\n")
    for i,t in enumerate(traffic):
        datfile.write("{} {}\n".format(i, t[0]))
    datfile.write(";\n")
    # traffic start node
    datfile.write("\n/* traffic matrix:target node */\n")
    datfile.write("param : TK :t:=\n")
    for i,t in enumerate(traffic):
        datfile.write("{} {}\n".format(i, t[1]))
    datfile.write(";\n")

    # DK
    datfile.write("\n/* traffic matrix:traffic demand */\n")
    datfile.write("param : DK :d:=\n")
    for i,t in enumerate(traffic):
        datfile.write("{} {}\n".format(i, 100.00))
    datfile.write(";\n")

    datfile.write("end;\n")

    datfile.close()

def to_coordinate_csv(britefile, output):
    """
    BRITEParserが提供するデータフォーマットからノードの位置座標を書き込んだcsvファイルを生成する
    """
    brite = BRITEParser(britefile)
    coordinates = DataFrame(brite.coordinates)
    coordinates.to_csv(output)
