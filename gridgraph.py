import random

import networkx as nx
import matplotlib.pyplot as plt


class GridGraph:

    def __init__(self, m, n, prob_to_remove_edge=0.0):
        assert prob_to_remove_edge >= 0 and prob_to_remove_edge < 0.4
        self.prob_to_remove_edge = prob_to_remove_edge
        self.m = m
        self.n = n
        self.nx_graph = self._grid_graph()
        self.node_pos = self._get_node_pos()

    def _grid_graph(self):
        """
        m×nの格子グラフを返す
        """
        m, n = self.m + 1, self.n + 1
        edges = []
        for v in range(1, m * n + 1):
            w = random.randint(1, 100)
            if v % n != 0:
                edges.append((v, v + 1, w))
            w = random.randint(1, 100)
            if v <= (m - 1) * n:
                edges.append((v, v + n, w))
        G = nx.Graph()
        G.add_weighted_edges_from(edges)
        return G

    def _get_node_pos(self):
        """
        ノードの位置座標を返す
        """
        n = sorted(self.nx_graph[1].keys())[1] - 1
        m = self.nx_graph.number_of_nodes() // n
        pos = {}
        for v in range(1, m * n + 1):
            pos[v] = ((v - 1) % n, (m * n - v) // n)
        return pos

    def draw(self, subgraph=None, edge_labels=None, optional_node_label=None):
        """
        格子グラフを描画する

        arguments:
        * subgraph(edgelist, optional)
          指定すると、その部分が赤く表示される
        * edge_labels(dict, optional)
        """
        nx.draw_networkx_nodes(self.nx_graph, self.node_pos, node_color='w')
        nx.draw_networkx_labels(self.nx_graph, self.node_pos)
        nx.draw_networkx_edges(self.nx_graph, self.node_pos)
        if edge_labels:
            nx.draw_networkx_edge_labels(self.nx_graph, self.node_pos, edge_labels=edge_labels, font_size=8)
        if subgraph is not None:
            subgraph = nx.Graph(data=subgraph)
            nx.draw_networkx_nodes(subgraph, self.node_pos, node_color='r')
            nx.draw_networkx_edges(subgraph, self.node_pos, edgelist=subgraph.edges(), edge_color='r', width=3.0)
            if edge_labels is not None:
                subgraph_metric = {(e[0],e[1]): edge_labels[e] for e in subgraph.edges()}
                nx.draw_networkx_edge_labels(subgraph, self.node_pos, edge_labels=subgraph_metric, font_color='r', font_size=8)
        if optional_node_label is not None:
            for node, num in optional_node_label.values():
                plt.text(self.node_pos[node][0]+0.1, self.node_pos[node][1]+0.2, num, fontsize=11)
        plt.xticks([])
        plt.yticks([])
