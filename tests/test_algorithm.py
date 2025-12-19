import unittest
from src.data_structure import MarketBasketGraph
from src.algorithms import MarketBasketAnalyser

class TestMarketBasketAnalyser(unittest.TestCase):
    def setUp(self):
        """Setup a graph with known data for testing."""
        self.graph = MarketBasketGraph()
        
        # --- Transaction Data Setup ---
        # 1. Milk + Bread (3 times)
        self.graph.add_transaction(['milk', 'bread'])
        self.graph.add_transaction(['milk', 'bread'])
        self.graph.add_transaction(['milk', 'bread'])
        
        # 2. Milk + Eggs (1 time)
        self.graph.add_transaction(['milk', 'eggs'])
        
        # 3. Beer + Diapers (2 times)
        self.graph.add_transaction(['beer', 'diapers'])
        self.graph.add_transaction(['beer', 'diapers'])
        
        # 4. Just Milk (1 time) - Total Milk transactions = 5
        self.graph.add_transaction(['milk'])
        
        # Total Transactions: 3 + 1 + 2 + 1 = 7
        # Total Items (Unique per basket):
        # (2*3) + (2*1) + (2*2) + (1*1) = 6 + 2 + 4 + 1 = 13 items total
        
        self.analyser = MarketBasketAnalyser(self.graph)

    # ==========================================
    # ASSIGNMENT BRIEF REQUIREMENTS
    # ==========================================

    def test_get_top_bundles(self):
        """Q1: Top 3 most common product bundles?"""
        top_bundles = self.analyser.get_top_bundles(n=2)
        
        # 1st: Milk+Bread (3)
        self.assertEqual(top_bundles[0], (('bread', 'milk'), 3))
        # 2nd: Beer+Diapers (2)
        self.assertEqual(top_bundles[1], (('beer', 'diapers'), 2))

    def test_get_frequent_associations(self):
        """Q2: Items frequently bought with [Bread]?"""
        associations = self.analyser.get_frequent_associations('milk')
        
        # Milk is connected to Bread (3) and Eggs (1)
        self.assertEqual(associations[0], ('bread', 3))
        self.assertEqual(associations[1], ('eggs', 1))

    def test_calculate_confidence(self):
        """Q3: Identify co-purchase likelihood (Probability Extension)."""
        # P(Bread | Milk) = 3 / 5 = 0.6
        confidence = self.analyser.calculate_confidence('milk', 'bread')
        self.assertEqual(confidence, 0.6)

    # ==========================================
    # INDUSTRY EXTENSIONS - from own experience
    # ==========================================

    def test_get_most_sold_item(self):
        """Extension: What is the single most sold item?"""
        # Milk appears in 5 transactions. Bread appears in 3.
        item, count = self.analyser.get_most_sold_item()
        
        self.assertEqual(item, 'milk')
        self.assertEqual(count, 5)

    def test_get_average_basket_size(self):
        """Extension: Average number items per basket (for store planning)."""
        # Total Items = 13
        # Total Transactions = 7
        # Average = 13 / 7 ≈ 1.857
        avg_size = self.analyser.get_average_basket_size()
        self.assertAlmostEqual(avg_size, 1.857, places=3)


    def test_bfs_recommendations(self):
        """
        Test BFS to find items 2 hops away.
        Scenario:
        - 'Gin' is connected to 'Tonic'
        - 'Tonic' is connected to 'Lemons'
        - 'Gin' is NOT connected directly to 'Lemons'
        
        BFS from 'Gin' should find 'Lemons' at depth 2.
        """
        # Setup specific graph for this test
        g = MarketBasketGraph()
        g.add_transaction(['gin', 'tonic'])
        g.add_transaction(['tonic', 'lemons'])
        
        analyser = MarketBasketAnalyser(g)
        
        # Get items within 2 hops of Gin
        recommendations = analyser.get_bfs_recommendations('gin', max_depth=2)
        
        # Recommendations should contain Lemons (depth 2) and Tonic (depth 1)
        self.assertIn('lemons', recommendations)
        self.assertIn('tonic', recommendations)
        
        # Ensure the start node is filtered out
        self.assertNotIn('gin', recommendations)

    def test_get_top_n_items(self):
        """
        Test that we can correctly identify the top N high-volume items.
        """
        
        # Ask for Top 3
        top_items = self.analyser.get_top_n_items(n=3)
        
        # Expectation: ['milk', 'bread', 'beer'] 
        
        self.assertEqual(len(top_items), 3)
        self.assertEqual(top_items[0], 'milk')  # 5 sales
        self.assertEqual(top_items[1], 'bread') # 3 sales
        
        # Verify the list contains the expected items
        self.assertIn('beer', top_items)

if __name__ == '__main__':
    unittest.main()