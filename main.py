import os
from src.loader import DataLoader
from src.data_structure import MarketBasketGraph
from src.algorithms import MarketBasketAnalyser

def main():
    # Configuration
    FILE_PATH = os.path.join('data', 'Supermarket_dataset_PAI.csv')
    
    print("="*50)
    print("MARKET BASKET ANALYSIS TOOL ")
    print("="*50)

    # Load Data
    print(f"\n[1] Loading data from {FILE_PATH}...")
    loader = DataLoader(FILE_PATH)
    transactions = loader.load_transactions()
    
    if not transactions:
        print("Error: No transactions found. Check your file path.")
        return

    print(f"-> Successfully loaded {len(transactions)} transactions.")

    # Build Graph
    print("\n[2] Building Graph Structure...")
    graph = MarketBasketGraph()
    for t in transactions:
        graph.add_transaction(t)
    
    print(f"-> Graph built with {len(graph.get_all_nodes())} unique items.")
    print(f"-> Total items processed: {graph.total_items_purchased}")

    # 3. Analyze
    analyzer = MarketBasketAnalyser(graph)

    # Q1: Top Bundles 
    print("\n" + "-"*40)
    print("Q1: Top 3 Most Common Product Bundles")
    print("-" * 40)
    top_bundles = analyzer.get_top_bundles(n=3)
    for rank, (pair, count) in enumerate(top_bundles, 1):
        print(f"   {rank}. {pair[0]} + {pair[1]} (Bought together {count} times)")

    # Q2: Recommendations for a Specific Item
    target_item = 'whole milk' # Common item in the dataset
    print("\n" + "-"*40)
    print(f"Q2: Frequent Co-purchases with '{target_item}'")
    print("-" * 40)
    associations = analyzer.get_frequent_associations(target_item)
    for item, count in associations[:3]:
        print(f"   -> Customers who buy '{target_item}' also buy '{item}' ({count} times)")

    # Q3: Probability/Confidence
    print("\n" + "-"*40)
    print("Q3: Strategic Insights")
    print("-" * 40)
    
    # Insight A: Most Sold
    best_item, best_count = analyzer.get_most_sold_item()
    print(f"   [Volume Driver] Best Selling Item: '{best_item}' ({best_count} sales)")
    
    # Insight B: Basket Size
    avg_size = analyzer.get_average_basket_size()
    print(f"   [Store Layout] Average Basket Size: {avg_size:.2f} items")
    
    # Insight C: Confidence Rule
    # "If they buy Whole Milk, how likely are they to buy Bread?"
    item_a = 'whole milk'
    item_b = 'rolls/buns' # Adjust based on data results
    confidence = analyzer.calculate_confidence(item_a, item_b)
    print(f" [Promotion] Confidence Rule: P({item_b} | {item_a}) = {confidence*100:.1f}%")
    print(f" (Meaning: {confidence*100:.1f}% of people who buy {item_a} also buy {item_b})")

    print("\n" + "="*50)
    print("Analysis Complete.")
    print("="*50)

if __name__ == "__main__":
    main()