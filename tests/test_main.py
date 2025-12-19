import unittest
from unittest.mock import patch
from main import main

class TestMainApplication(unittest.TestCase):
    
    @patch('main.DataLoader') 
    @patch('builtins.print')
    def test_main_execution_flow(self, mock_print, MockLoader):
        """
        Smoke Test: Ensure main() runs from start to finish without crashing.
        Mock the data so don't need the real CSV file.
        """
        
        # Setup the Fake Loader to return simple dummy data
        mock_loader_instance = MockLoader.return_value
        mock_loader_instance.load_transactions.return_value = [
            ['milk', 'bread'],
            ['milk', 'eggs'],
            ['milk', 'bread']
        ]

        # Run application
        try:
            main()
        except Exception as e:
            self.fail(f"main() crashed with an error: {e}")

        # Assertions

    
        MockLoader.assert_called() 
        
        # Did it reach the end? 
        printed_messages = [str(call) for call in mock_print.mock_calls]
        found_completion = any("Analysis Complete" in msg for msg in printed_messages)
        
        self.assertTrue(found_completion, "The application did not reach the 'Analysis Complete' stage.")

if __name__ == '__main__':
    unittest.main()
