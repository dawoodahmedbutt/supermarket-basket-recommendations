import os
from src.loader import DataLoader
from src.data_structure import MarketBasketGraph
from src.algorithms import MarketBasketAnalyser
from src.visualisation import GraphVisualiser

def main():
    FILE_PATH = os.path.join('data', 'Supermarket_dataset_PAI.csv')
    
    print("="*50)
    print("     MARKET BASKET ANALYSIS TOOL (Task 2)")
    print("="*50)

    # Load & Build
    print(f"\n[1] Loading data...")
    loader = DataLoader(FILE_PATH)
    transactions = loader.load_transactions()
    
    if not transactions:
        return

    graph = MarketBasketGraph()
    for t in transactions:
        graph.add_transaction(t)
    
    analyser = MarketBasketAnalyser(graph)

    # Q1 & Q2
    print("\n" + "-"*40)
    print("Q1: Top 3 Bundles (Global)")
    print("-" * 40)
    top = analyser.get_top_bundles(3)
    for pair, count in top:
        print(f"   {pair[0]} + {pair[1]}: {count}")

    target = 'yogurt' 
    print("\n" + "-"*40)
    print(f"Q2: Associations for '{target}'")
    print("-" * 40)
    assoc = analyser.get_frequent_associations(target)
    for item, count in assoc[:3]:
        print(f"   {item} (Bought together {count} times)")

    # BFS Recommendation 
    print("\n" + "-"*40)
    print(f"Q4: BFS Recommendations for '{target}'")
    print("    (Finding indirect connections 2 hops away)")
    print("-" * 40)
    
    bfs_recs = analyser.get_bfs_recommendations(target, max_depth=2)
    # Filter out immediate neighbors to show new discoveries
    direct_neighbors = [x[0] for x in assoc]
    indirect = [item for item in bfs_recs if item not in direct_neighbors and item != target]
    
    print(f"   Found {len(indirect)} indirect connections. Top samples:")
    print(f"   {indirect[:5]}")

    # Visualisation
    print("\n" + "-"*40)
    print("[5] Generating Graph Plot...")
    vis = GraphVisualiser(graph)
    # filter edges < 100 co-occurrences to keep the plot readable
    vis.plot_top_associations(min_weight=100, output_file="market_graph.png")

if __name__ == "__main__":
    main()