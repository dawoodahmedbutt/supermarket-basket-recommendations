import unittest
import os
import csv
from src.loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """Create a temporary CSV file for testing."""
        self.test_file = 'test_data.csv'
        with open(self.test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Member_number', 'Date', 'itemDescription'])

            # Scenario: Member 1001 buys milk and bread on 01-01-2015
            # this should be grouped into ONE transaction.
            writer.writerow(['1001', '01-01-2015', 'milk'])
            writer.writerow(['1001', '01-01-2015', 'bread'])

            # Scenario: Member 1002 buys soda on 02-01-2015
            # This is a new separate transaction.
            writer.writerow(['1002', '02-01-2015', 'soda'])

            # Scenario: Member 1001 buys beer on 05-01-2015
            # Same member, different date -> NEW transaction.
            writer.writerow(['1001', '05-01-2015', 'canned beer'])

    def tearDown(self):
        """Clean up the temporary file after tests run."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_transactions_grouping(self):
        loader = DataLoader(self.test_file)
        transactions = loader.load_transactions()

        # We expect 3 unique transactions from the data above
        self.assertEqual(len(transactions), 3)

        # Find the transaction containing 'milk' and ensure 'bread' is with it
        # This confirms the grouping logic works
        milk_transaction = next(t for t in transactions if 'milk' in t)
        self.assertIn('bread', milk_transaction)
        self.assertEqual(len(milk_transaction), 2)

    def test_file_not_found(self):
        """Test how the loader handles a missing file."""
        loader = DataLoader("non_existent.csv")
        transactions = loader.load_transactions()
        self.assertEqual(transactions, [])

if __name__ == '__main__':
    unittest.main()