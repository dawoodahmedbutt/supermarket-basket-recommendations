import os
from src.loader import DataLoader
from src.data_structure import MarketBasketGraph
from src.algorithms import MarketBasketAnalyser
from src.visualisation import GraphVisualiser

def main():
    # --- Configuration ---
    FILE_PATH = os.path.join('data', 'Supermarket_dataset_PAI.csv')
    
    print("="*50)
    print("     MARKET BASKET ANALYSIS TOOL (Task 2)")
    print("="*50)

    # 1. Load Data
    print(f"\n[1] Loading data...")
    loader = DataLoader(FILE_PATH)
    transactions = loader.load_transactions()
    
    if not transactions:
        print("Error: No transactions found.")
        return

    # 2. Build Graph
    graph = MarketBasketGraph()
    for t in transactions:
        graph.add_transaction(t)
    
    # 3. Initialise Analyser & Visualiser
    analyser = MarketBasketAnalyser(graph)
    vis = GraphVisualiser(graph)

    # Q1: Top Bundles
    print("\n" + "-"*40)
    print("Q1: Top 5 Bundles (Global)")
    print("-" * 40)
    top_bundles = analyser.get_top_bundles(n=5)
    for pair, count in top_bundles:
        print(f"   {pair[0]} + {pair[1]}: {count}")

    # Q2: Direct Recommendations
    target_item = 'yogurt' # can change this to any item
    print("\n" + "-"*40)
    print(f"Q2: Associations for '{target_item}'")
    print("-" * 40)
    associations = analyser.get_frequent_associations(target_item)
    for item, count in associations[:3]:
        print(f"   {item} (Bought together {count} times)")

    # Q3: Strategic Insights 
    print("\n" + "-"*40)
    print("Q3: Strategic Insights (Data-Driven Decisions)")
    print("-" * 40)
    
    best_item, best_count = analyser.get_most_sold_item()
    print(f"   [Volume Driver] Best Selling Item: '{best_item}' ({best_count} sales)")
    
    avg_size = analyser.get_average_basket_size()
    print(f"   [Store Layout] Average Basket Size: {avg_size:.2f} items")
    
    print(f"\n   [Promotion] Top Cross-Sell Opportunities (Smart Filtered):")
    
    opportunities = analyser.get_strategic_cross_sells(top_n=5)
    
    for i, (driver, partner, conf) in enumerate(opportunities, 1):
        if partner:
            print(f"      {i}. Driver: '{driver}' -> Promote: '{partner}'")
            print(f"          (Confidence: {conf*100:.1f}%)")
        else:
            print(f"      {i}. Driver: '{driver}' -> (No niche partner found)")

    # Q4: BFS Recommendations
    print("\n" + "-"*40)
    print(f"Q4: BFS Recommendations for '{target_item}'")
    print("    (Finding 'Hidden' Connections 2 hops away)")
    print("-" * 40)
    
    niche_recs = analyser.get_niche_bfs_recommendations(target_item, max_depth=2)
    
    print(f"   Context: Analysis removed 'Mega Hubs' to find niche clusters.")
    print(f"   Found {len(niche_recs)} niche connections. Top samples:")
    print(f"   {niche_recs[:5]}")

    # VISUALISATION 1: Global 
    print("\n" + "-"*40)
    print("[5] Generating Global Network Plot...")
    vis.plot_top_associations(min_weight=50, output_file="market_graph_global.png")

    # VISUALISATION 2: Top 10 Ego Graphs 
    print("\n" + "-"*40)
    print("[6] Generating Strategic Visualisation Report (Top 10 Items)")
    print("-" * 40)
    
    if not os.path.exists('report_images'):
        os.makedirs('report_images')
        
    top_10 = analyser.get_top_n_items(10)
    print(f"   Generating analysis for: {top_10}")
    
    for rank, item in enumerate(top_10, 1):
        safe_name = item.replace('/', '_')
        filename = f"report_images/rank_{rank}_{safe_name}.png"
        
        print(f"   -> Ego Graph saved: {filename}")
        vis.plot_ego_graph(item, filename)

    print("\n" + "="*50)
    print("Analysis Complete.")
    print("="*50)

if __name__ == "__main__":
    main()