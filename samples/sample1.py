"""
cost239のモデルデータを読み込んで双方向リンクを考慮してGraphillionでパス列挙する
"""

from graphillion import GraphSet
import utils
utils.expand_load_path(__file__)
import directed_link as dl
from dat_utils import Dat
from drawing import *

set_default_coordinate_path("../../model_data_coordinates/")
set_default_model_path("../../model_data/")

cost239 = Dat("../../model_data/COST239/COST239_EQ_200.dat")
dl.read_edgelist(cost239.cost)
GraphSet.set_universe(dl.append_virtual_nodes())

paths = GraphSet.paths(0, 10)
for i,path in enumerate(paths):
    print(dl.original_path(path))
    if i == 9: break

draw_model_data("cost239", path=dl.original_path(paths.choice()))
