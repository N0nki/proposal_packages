"""
author Mio Kinno
date 2017.8.30
branch master
file test_directed_link.py

以下のグラフを使用する
ただし，リンクは双方向とする
1----2
|   /|
|  / |
| /  |
|/   |
3----4
"""

from nose.tools import ok_, eq_, raises, with_setup
from graphillion import GraphSet
import proposal_packages.directed_link as dl

class TestDirectedLink:

    edgelist = [(1,2,10),(1,3,20),(2,3,30),(2,4,40),(3,4,50),
                (2,1,10),(3,1,20),(3,2,30),(4,2,40),(4,3,50)]

    def setup(self):
        dl.read_edgelist(self.edgelist)
        GraphSet.set_universe(dl.append_virtual_nodes())

    def teardown(self):
        pass

    def test_append_virtual_nodes(self):
        eq_(dl.append_virtual_nodes(),[(1, 2, 10), (2, 2100, 10), (2100, 1, 0), (1, 3, 20), (3, 3100, 20), (3100, 1, 0), (2, 3, 30), (3, 3200, 30), (3200, 2, 0), (2, 4, 40), (4, 4200, 40), (4200, 2, 0), (3, 4, 50), (4, 4300, 50), (4300, 3, 0)])
    
    def test_edges_table(self):
        eq_(dl.edges_table(), {(1, 2): [(1, 2, 10), (2, 1, 10)], (1, 3): [(1, 3, 20), (3, 1, 20)], (2, 3): [(2, 3, 30), (3, 2, 30)], (2, 4): [(2, 4, 40), (4, 2, 40)], (3, 4): [(3, 4, 50), (4, 3, 50)]})

    def test_virtual_nodes_expression(self):
        eq_(dl.virtual_node_expression(2, 1), 2100)
        eq_(dl.virtual_node_expression(3, 1), 3100)
        eq_(dl.virtual_node_expression(3, 2), 3200)
        eq_(dl.virtual_node_expression(4, 2), 4200)
        eq_(dl.virtual_node_expression(4, 3), 4300)

    def test_devide_virtual_node(self):
        eq_(dl.devide_virtual_node(2100), (2, 1))
        eq_(dl.devide_virtual_node(3100), (3, 1))
        eq_(dl.devide_virtual_node(3200), (3, 2))
        eq_(dl.devide_virtual_node(4200), (4, 2))
        eq_(dl.devide_virtual_node(4300), (4, 3))

    def test_virtual_node_edges(self):
        eq_(dl.virtual_node_edges(), [[(2, 2100)], [(2100, 1)], [(3, 3100)], [(3100, 1)], [(3, 3200)], [(3200, 2)], [(4, 4200)], [(4200, 2)], [(4, 4300)], [(4300, 3)]])

    def test_virtual_nodes(self):
        eq_(dl.virtual_nodes(), [2100, 3100, 3200, 4200, 4300])

    def test_original_noses(self):
        eq_(dl.original_nodes(), [1, 2, 3, 4])

    def test_predecessor_nodes(self):
        eq_(dl.predecessor_nodes(1), [2100, 3100])
        eq_(dl.predecessor_nodes(2), [1, 3200, 4200])
        eq_(dl.predecessor_nodes(3), [1, 2, 4300])
        eq_(dl.predecessor_nodes(4), [2, 3])

    def test_neighbor_nodes(self):
        neighbors1 = dl.neighbor_nodes(1)
        for node in [2, 3]:
            ok_(node in neighbors1)

        neighbors2 = dl.neighbor_nodes(2)
        for node in [2100, 3, 4]:
            ok_(node in neighbors2)

        neighbors3 = dl.neighbor_nodes(3)
        for node in [3100, 3200, 4]:
            ok_(node in neighbors3)

        neighbors4 = dl.neighbor_nodes(4)
        for node in [4200, 4300]:
            ok_(node in neighbors4)

    def test_external_edges(self):
        external1 = dl.external_edges(1)
        for edge in [[(1,2)], [(1,3)]]:
            ok_(edge in external1)

        external2 = dl.external_edges(2)
        for edge in [[(2,2100)], [(2,4)], [(2,3)]]:
            ok_(edge in external2)

        external3 = dl.external_edges(3)
        for edge in [[(3,3100)], [(3,4)]]:
            ok_(edge in external3)

        external4 = dl.external_edges(4)
        for edge in [[(4,4200)], [(4,4300)]]:
            ok_(edge in external4)

    def test_original_path(self):
        pass

    def test_internal_edges(self):
        internal1 = dl.internal_edges(1)
        for edge in[[(2100,1)], [(3100,1)]]:
            ok_(edge in internal1)

        internal2 = dl.internal_edges(2)
        for edge in[[(1,2)], [(3200,2)], [(4200,2)]]:
            ok_(edge in internal2)

        internal3 = dl.internal_edges(3)
        for edge in[[(1,3)], [(2,3)], [(4300,3)]]:
            ok_(edge in internal3)

        internal4 = dl.internal_edges(4)
        for edge in[[(2,4)], [(3,4)]]:
            ok_(edge in internal4)

    def test_two_internal_edges_subgraph(self):
        subgraphs1 = dl.two_internal_edges_subgraph(1)
        for subgraph in [[(2100,1), (3100, 1)]]:
            ok_(subgraph in subgraphs1)

        subgraphs2 = dl.two_internal_edges_subgraph(2)
        for subgraph in [[(1,2), (3200,2)], [(1,2), (4200,2)], [(3200,2), (4200,2)]]:
            ok_(subgraph in subgraphs2)

        subgraphs3 = dl.two_internal_edges_subgraph(3)
        for subgraph in [[(1,3), (2,3)], [(1,3), (4300,3)], [(2,3), (4300,3)]]:
            ok_(subgraph in subgraphs3)

        subgraphs4 = dl.two_internal_edges_subgraph(4)
        for subgraph in [[(2,4), (3,4)]]:
            ok_(subgraph in subgraphs4)

    def test_invalid_direction_elms(self):
        subgraphs12 = dl.invalid_direction_elms(1, 2)
        for subgraph in [[(2100, 1)], [(3100, 1)], [(1, 3), (2, 3)], [(1, 3), (4300, 3)], [(2, 3), (4300, 3)], [(2, 4), (3, 4)]]:
            ok_(subgraph in subgraphs12)

        subgraphs13 = dl.invalid_direction_elms(1, 3)
        for subgraph in [[(2100, 1)], [(3100, 1)], [(1, 2), (3200, 2)], [(1, 2), (4200, 2)], [(3200, 2), (4200, 2)], [(2, 4), (3, 4)]]:
            ok_(subgraph in subgraphs13)

        subgraphs14 = dl.invalid_direction_elms(1, 4)
        for subgraph in [[(2100, 1)], [(3100, 1)], [(1, 2), (3200, 2)], [(1, 2), (4200, 2)], [(3200, 2), (4200, 2)], [(1, 3), (2, 3)], [(1, 3), (4300, 3)], [(2, 3), (4300, 3)]]:
            ok_(subgraph in subgraphs14)

        subgraphs21 = dl.invalid_direction_elms(2, 1)
        for subgraph in [[(1, 2)], [(3200, 2)], [(4200, 2)], [(1, 3), (2, 3)], [(1, 3), (4300, 3)], [(2, 3), (4300, 3)], [(2, 4), (3, 4)]]:
            ok_(subgraph in subgraphs21)

        subgraphs23 = dl.invalid_direction_elms(2, 3)
        for subgraph in [[(1, 2)], [(3200, 2)], [(4200, 2)], [(2100, 1), (3100, 1)], [(2, 4), (3, 4)]]:
            ok_(subgraph in subgraphs23)

        subgraphs24 = dl.invalid_direction_elms(2, 4)
        for subgraph in [[(1, 2)], [(3200, 2)], [(4200, 2)], [(2100, 1), (3100, 1)], [(1, 3), (2, 3)], [(1, 3), (4300, 3)], [(2, 3), (4300, 3)]]:
            ok_(subgraph in subgraphs24)

        subgraphs31 = dl.invalid_direction_elms(3, 1)
        for subgraph in [[(1, 3)], [(2, 3)], [(4300, 3)], [(1, 2), (3200, 2)], [(1, 2), (4200, 2)], [(3200, 2), (4200, 2)], [(2, 4), (3, 4)]]:
            ok_(subgraph in subgraphs31)

        subgraphs32 = dl.invalid_direction_elms(3, 2)
        for subgraph in [[(1, 3)], [(2, 3)], [(4300, 3)], [(2100, 1), (3100, 1)], [(2, 4), (3, 4)]]:
            ok_(subgraph in subgraphs32)

        subgraphs34 = dl.invalid_direction_elms(3, 4)
        for subgraph in [[(1, 3)], [(2, 3)], [(4300, 3)], [(2100, 1), (3100, 1)], [(1, 2), (3200, 2)], [(1, 2), (4200, 2)], [(3200, 2), (4200, 2)]]:
            ok_(subgraph in subgraphs34)

        subgraphs41 = dl.invalid_direction_elms(4, 1)
        for subgraph in [[(2, 4)], [(3, 4)], [(1, 2), (3200, 2)], [(1, 2), (4200, 2)], [(3200, 2), (4200, 2)], [(1, 3), (2, 3)], [(1, 3), (4300, 3)], [(2, 3), (4300, 3)]]:
            ok_(subgraph in subgraphs41)

        subgraphs42 = dl.invalid_direction_elms(4, 2)
        for subgraph in [[(2, 4)], [(3, 4)], [(2100, 1), (3100, 1)], [(1, 3), (2, 3)], [(1, 3), (4300, 3)], [(2, 3), (4300, 3)]]:
            ok_(subgraph in subgraphs42)

        subgraphs43 = dl.invalid_direction_elms(4, 3)
        for subgraph in [[(2, 4)], [(3, 4)], [(2100, 1), (3100, 1)], [(1, 2), (3200, 2)], [(1, 2), (4200, 2)], [(3200, 2), (4200, 2)]]:
            ok_(subgraph in subgraphs43)

    def test_directed_paths(self):
        pass
