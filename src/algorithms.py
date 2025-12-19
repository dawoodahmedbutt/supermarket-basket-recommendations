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

    # Extension questions
    def get_most_sold_item(self):
        """Extension: Single most sold item."""
        nodes = self.graph.get_all_nodes()
        if not nodes: return None, 0
        
        # Convert to list of (item, frequency)
        node_freqs = [(node, self.graph.get_node_frequency(node)) for node in nodes]
        
        # Sort to find top
        self._bubble_sort_descending(node_freqs)
        return node_freqs[0]

    def get_average_basket_size(self):
        """Extension: Average items per basket."""
        if self.graph.total_transactions == 0:
            return 0.0
        return self.graph.total_items_purchased / self.graph.total_transactions

    # Helper function
    
    def _bubble_sort_descending(self, items):
        """Sorts list of tuples [(data, weight), ...] by weight descending."""
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if items[j][1] < items[j + 1][1]:
                    items[j], items[j + 1] = items[j + 1], items[j]


    # BFS traversal
    def get_bfs_recommendations(self, start_item, max_depth=2):
        """
        Uses Breadth-First Search (BFS) to find related items up to `max_depth` hops away.
        """
        visited = set()
        queue = deque([(start_item, 0)])  
        visited.add(start_item)
        
        recommendations = set()

        while queue:
            current_node, depth = queue.popleft()
            
            if depth >= max_depth:
                continue
            
            # Get neighbors from the graph
            neighbors = self.graph.get_neighbors(current_node)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    recommendations.add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        return list(recommendations)