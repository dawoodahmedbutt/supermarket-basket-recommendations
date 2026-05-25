from collections import deque


class MarketBasketAnalyser:
    def __init__(self, graph):
        self.graph = graph

    def get_top_bundles(self, n=3):
        """Q1: Top product bundles (Bubble Sort)."""
        all_edges = []
        processed = set()
        
        nodes = self.graph.get_all_nodes()
        for node in nodes:
            neighbors = self.graph.get_neighbors(node)
            for neighbor, weight in neighbors.items():
                pair = tuple(sorted((node, neighbor)))
                if pair not in processed:
                    all_edges.append((pair, weight))
                    processed.add(pair)
        
        self._bubble_sort_descending(all_edges)
        return all_edges[:n]

    def get_frequent_associations(self, item):
        """Q2: Items bought with X (Bubble Sort)."""
        neighbors = self.graph.get_neighbors(item)
        associations = list(neighbors.items())
        self._bubble_sort_descending(associations)
        return associations

    def calculate_confidence(self, item_a, item_b):
        """Q3: P(B|A) - Confidence."""
        count_a = self.graph.get_node_frequency(item_a)
        if count_a == 0: return 0.0
        return self.graph.get_edge_weight(item_a, item_b) / count_a

    def get_most_sold_item(self):
        """Extension: Single most sold item."""
        nodes = self.graph.get_all_nodes()
        if not nodes:
            return None, 0
        node_freqs = [(node, self.graph.get_node_frequency(node)) for node in nodes]
        self._bubble_sort_descending(node_freqs)
        return node_freqs[0]

    def get_average_basket_size(self):
        """Extension: Average items per basket."""
        if self.graph.total_transactions == 0:
            return 0.0
        return self.graph.total_items_purchased / self.graph.total_transactions

    def _bubble_sort_descending(self, items):
        """Sorts list of tuples [(data, weight), ...] by weight descending."""
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if items[j][1] < items[j + 1][1]:
                    items[j], items[j + 1] = items[j + 1], items[j]

    def get_bfs_recommendations(self, start_item, max_depth=2):
        """BFS from start_item — returns all items reachable within max_depth hops."""
        visited = {start_item}
        queue = deque([(start_item, 0)])
        recommendations = set()

        while queue:
            current_node, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for neighbor in self.graph.get_neighbors(current_node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    recommendations.add(neighbor)
                    queue.append((neighbor, depth + 1))

        return list(recommendations)

    def get_top_n_items(self, n=10):
        """Returns the names of the top N most frequent items."""
        nodes = self.graph.get_all_nodes()
        # Secondary sort by name ensures a stable, deterministic order on ties
        ranked = sorted(
            [(node, self.graph.get_node_frequency(node)) for node in nodes],
            key=lambda x: (-x[1], x[0])
        )
        return [item[0] for item in ranked[:n]]

    def get_strategic_cross_sells(self, top_n=5, commodity_items=None):
        """
        Returns (Driver, Promote_Item, Confidence) tuples for the top N volume drivers.
        Skips commodity items as promotion targets — they're already in most baskets
        and promoting them adds no uplift.
        """
        if commodity_items is None:
            commodity_items = ['whole milk', 'other vegetables', 'rolls/buns', 'soda', 'yogurt', 'root vegetables']

        top_drivers = self.get_top_n_items(top_n)
        results = []

        for driver in top_drivers:
            partners = self.get_frequent_associations(driver)
            selected_partner = None
            for partner, count in partners:
                if partner not in commodity_items:
                    selected_partner = partner
                    break
            if selected_partner:
                conf = self.calculate_confidence(driver, selected_partner)
                results.append((driver, selected_partner, conf))
            else:
                results.append((driver, None, 0.0))

        results.sort(key=lambda x: x[2], reverse=True)
        return results

    def get_niche_bfs_recommendations(self, start_item, max_depth=2, filter_hubs=None):
        """
        BFS from start_item, filtered to indirect (non-adjacent) items only.
        Removes high-degree hub nodes that appear in almost every result set.
        """
        if filter_hubs is None:
            filter_hubs = ['whole milk', 'other vegetables', 'rolls/buns', 'soda']

        raw_recs = self.get_bfs_recommendations(start_item, max_depth)
        direct_neighbors = {x[0] for x in self.get_frequent_associations(start_item)}

        return [
            item for item in raw_recs
            if item != start_item
            and item not in direct_neighbors
            and item not in filter_hubs
        ]