"""CSV loading utilities for supermarket transaction data."""

import csv
from collections import defaultdict


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_transactions(self):
        """
        Read the CSV and group rows by (Member_number, Date) into transactions.
        Returns a list of lists, e.g. [['milk', 'bread'], ['soda'], ...]
        """
        grouped_data = defaultdict(list)

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    member = row['Member_number'].strip()
                    date = row['Date'].strip()
                    item = row['itemDescription'].strip()
                    grouped_data[(member, date)].append(item)

            return list(grouped_data.values())

        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return []
        except Exception as e:
            print(f"An error occurred loading data: {e}")
            return []
