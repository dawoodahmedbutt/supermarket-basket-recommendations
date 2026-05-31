"""Weighted graph data structure for market-basket transactions."""

from collections import defaultdict
import itertools


class MarketBasketGraph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.nodes = set()
        self.node_counts = defaultdict(int)
        self.total_transactions = 0
        self.total_items_purchased = 0

    def add_transaction(self, items):
        unique_items = sorted(list(set(items)))

        self.total_transactions += 1
        self.total_items_purchased += len(unique_items)

        for item in unique_items:
            self.nodes.add(item)
            self.node_counts[item] += 1

        for item1, item2 in itertools.combinations(unique_items, 2):
            self._add_edge(item1, item2)

    def _add_edge(self, u, v):
        self.graph[u][v] += 1
        self.graph[v][u] += 1

    def has_edge(self, u, v):
        return v in self.graph[u]

    def get_edge_weight(self, u, v):
        return self.graph[u].get(v, 0)

    def get_neighbors(self, node):
        return dict(self.graph[node])

    def get_all_nodes(self):
        """Return nodes in a stable order for reproducible rankings and plots."""
        return sorted(self.nodes)

    def get_node_frequency(self, node):
        return self.node_counts.get(node, 0)
