"""
author Mio Kinno
date 2018.8.2
branch master
file test_directed_link.py

以下のグラフを使用する
1----2
|   /|
|  / |
| /  |
|/   |
3----4
"""

from nose.tools import ok_, eq_, raises, with_setup
from graphillion import GraphSet
import proposal_packages.graphillion_utils as gu

class TestGraphillionUtils:
    edgelist = [(1,2,10), (1,3,20), (2,3,30), (2,4,40), (3,4,50)]

    def setup(self):
        GraphSet.set_universe(self.edgelist)

    def teardown(self):
        pass

    def test_degree(self):
        eq_(gu.degree(1), 2)
        eq_(gu.degree(2), 3)
        eq_(gu.degree(3), 3)
        eq_(gu.degree(4), 2)

    def test_flatten_paths(self):
        paths = GraphSet.paths(1, 4)
        edges = []
        for path in paths:
            for edge in path:
                edges.append(edge)
        eq_(gu.flatten_paths(paths), edges)

    def test_min_hop(self):
        eq_(gu.min_hop((1, 4)), 2)


    def test_max_hop(self):
        eq_(gu.max_hop((1, 4)), 3)

    def test_get_min_hop_paths(self):
        pass

    def test_excluding_multi_elms(self):
        pass

    def test_select_sleep_nodes(self):
        pass

    def test_hamming(self):
        pass

    def test_get_similar_paths(self):
        pass
