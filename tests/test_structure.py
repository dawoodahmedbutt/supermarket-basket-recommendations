import unittest
from src.data_structure import MarketBasketGraph

class TestMarketBasketGraph(unittest.TestCase):
    def setUp(self):
        """Runs before every test. Sets up a fresh graph instance."""
        self.graph = MarketBasketGraph()

    def test_add_transaction_creates_nodes(self):
        """Test that items from a transaction are added as nodes."""
        transaction = ['milk', 'bread']
        self.graph.add_transaction(transaction)
        
        # Check if nodes exist in the graph
        self.assertIn('milk', self.graph.get_all_nodes())
        self.assertIn('bread', self.graph.get_all_nodes())

    def test_add_transaction_creates_edge(self):
        """Test that items bought together form an edge."""
        transaction = ['milk', 'bread']
        self.graph.add_transaction(transaction)
        
        # Check if edge exists between milk and bread
        self.assertTrue(self.graph.has_edge('milk', 'bread'))
        
        # Check specific weight (should be 1 for the first occurrence)
        self.assertEqual(self.graph.get_edge_weight('milk', 'bread'), 1)

    def test_edge_weight_increments(self):
        """Test that frequency increases when pairs appear again."""
        # Transaction 1: milk + bread
        self.graph.add_transaction(['milk', 'bread', 'eggs'])
        # Transaction 2: milk + bread (again)
        self.graph.add_transaction(['milk', 'bread', 'apple'])
        
        # Milk-Bread appeared twice, so weight should be 2
        self.assertEqual(self.graph.get_edge_weight('milk', 'bread'), 2)
        # Milk-Eggs appeared once
        self.assertEqual(self.graph.get_edge_weight('milk', 'eggs'), 1)

    def test_get_neighbors(self):
        """Test retrieving associated items."""
        self.graph.add_transaction(['milk', 'bread', 'butter'])
        neighbors = self.graph.get_neighbors('milk')
        
        # Milk was bought with bread and butter
        self.assertIn('bread', neighbors)
        self.assertIn('butter', neighbors)
        self.assertEqual(neighbors['bread'], 1)

    def test_get_node_frequency(self):
        """Test that the graph counts the total occurrences of specific items."""
        # Transaction 1: Milk and Bread
        self.graph.add_transaction(['milk', 'bread'])
        
        # Transaction 2: Milk and Eggs
        self.graph.add_transaction(['milk', 'eggs'])
        
        # Transaction 3: Just Milk 
        self.graph.add_transaction(['milk'])

        # Milk appeared in 3 transactions total
        self.assertEqual(self.graph.get_node_frequency('milk'), 3)
        
        # Bread only appeared in 1
        self.assertEqual(self.graph.get_node_frequency('bread'), 1)
        
        # gold has never been bought
        self.assertEqual(self.graph.get_node_frequency('gold'), 0)


if __name__ == '__main__':
    unittest.main()