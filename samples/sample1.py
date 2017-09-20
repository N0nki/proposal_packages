"""
cost239のモデルデータを読み込んで双方向リンクを考慮してGraphillionでパス列挙する
"""

from graphillion import GraphSet
import utils
utils.expand_load_path(__file__)
import directed_link as dl
from dat_utils import Dat
from drawing import *

# model_data_coordinatesとmodel_dataへのパスを設定
set_default_coordinate_path("../../model_data_coordinates/")
set_default_model_path("../../model_data/")

# Datオブジェクト作成とユニバース設定
cost239 = Dat("../../model_data/COST239/COST239_EQ_200.dat")
dl.read_edgelist(cost239.cost)
GraphSet.set_universe(dl.append_virtual_nodes())

# 任意順序で列挙
paths = GraphSet.paths(0, 10)
for i,path in enumerate(paths):
    print(dl.original_path(path))
    if i == 9: break

# 昇順列挙
metric_table = {(i,j): w for i,j,w in dl.append_virtual_nodes()}
for i,path in enumerate(paths.min_iter(metric_table)):
    print(dl.original_path(path), dl.total_cost(metric_table, path))
    if i == 9: break

draw_model_data("cost239", path=dl.original_path(paths.choice()))
