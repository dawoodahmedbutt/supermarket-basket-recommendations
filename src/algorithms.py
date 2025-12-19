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

    def get_top_n_items(self, n=10):
        """Returns the names of the top N most frequent items."""
        nodes = self.graph.get_all_nodes()
        
        # Sort logic: 
        # Primary Key: Count (Descending) -> represented as -x[1]
        # Secondary Key: Name (Ascending/Alphabetical) -> represented as x[0]
        ranked = sorted(
            [(node, self.graph.get_node_frequency(node)) for node in nodes],
            key=lambda x: (-x[1], x[0])
        )
        
        return [item[0] for item in ranked[:n]]

    # Business logic
    def get_strategic_cross_sells(self, top_n=5, commodity_items=None):
        """
        Returns a list of (Driver, Promote_Item, Confidence) tuples.
        Applies Business Logic: If a Driver is a 'Commodity' (e.g. Milk),
        we look for the best partner that isn't also a commodity.
        """
        if commodity_items is None:
            # Default list of items to filter out if they appear as targets
            commodity_items = ['whole milk', 'other vegetables', 'rolls/buns', 'soda']

        top_drivers = self.get_top_n_items(top_n)
        results = []

        for driver in top_drivers:
            partners = self.get_frequent_associations(driver)
            
            selected_partner = None
            for partner, count in partners:
                # LOGIC: If driver is NOT a commodity, don't recommend a commodity.
                # If driver IS a commodity (e.g. Milk), we recommend the next best thing.
                if driver not in commodity_items and partner in commodity_items:
                    continue 
                
                selected_partner = partner
                break
            
            if selected_partner:
                conf = self.calculate_confidence(driver, selected_partner)
                results.append((driver, selected_partner, conf))
            else:
                results.append((driver, None, 0.0))
        
        return results

    def get_niche_bfs_recommendations(self, start_item, max_depth=2, filter_hubs=None):
        """
        Performs BFS but filters out 'Mega Hubs' from the results 
        to find interesting, niche connections.
        """
        if filter_hubs is None:
            filter_hubs = ['whole milk', 'other vegetables', 'rolls/buns', 'soda']

        # Get raw BFS results
        raw_recs = self.get_bfs_recommendations(start_item, max_depth)
        
        # Get direct neighbors (to exclude them)
        direct_assocs = self.get_frequent_associations(start_item)
        direct_neighbors = [x[0] for x in direct_assocs]
        
        # Filter
        clean_results = []
        for item in raw_recs:
            # Condition 1: Not the item itself
            if item == start_item: continue
            # Condition 2: Not a direct neighbor (we want indirect)
            if item in direct_neighbors: continue
            # Condition 3: Not a Mega Hub 
            if item in filter_hubs: continue
            
            clean_results.append(item)
            
        return clean_results