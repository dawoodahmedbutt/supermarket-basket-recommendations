import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualiser:
    def __init__(self, graph):
        self.graph_data = graph

    def plot_top_associations(self, min_weight=50, output_file="market_graph.png"):
        """
        Plot the graph with Node Counts and Edge Weights.
        """
        G = nx.Graph()

        # Build NetworkX graph
        nodes = self.graph_data.get_all_nodes()
        
        # Need to track which nodes actually get added (have edges > min_weight)
        active_nodes = set()

        for node in nodes:
            neighbors = self.graph_data.get_neighbors(node)
            for neighbor, weight in neighbors.items():
                if weight >= min_weight:
                    G.add_edge(node, neighbor, weight=weight)
                    active_nodes.add(node)
                    active_nodes.add(neighbor)

        # Setup Labels (Name + Count)
        node_labels = {}
        for node in active_nodes:
            count = self.graph_data.get_node_frequency(node)
            node_labels[node] = f"{node}\n({count})"

        # Setup Plot
        plt.figure(figsize=(14, 12)) 
        
        # "k" controls the spacing. Smaller k = tighter, Larger k = more spread out.
        pos = nx.spring_layout(G, k=0.5, seed=42)

        # Draw Nodes
        nx.draw_networkx_nodes(G, pos, node_size=2500, node_color='lightgreen', alpha=0.9)
        
        # Draw Node Labels with counts
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9, font_family='sans-serif', font_weight='bold')
        
        # Draw Edges
        edges = G.edges(data=True)
        # Scale width: weight 50 -> width 1, weight 200 -> width 4
        widths = [data['weight'] * 0.02 for _, _, data in edges]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color='gray', alpha=0.4)
        
        # Draw Edge Labels 
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

        plt.title(f"Supermarket Network (Strong Links > {min_weight} Transactions)", fontsize=16)
        plt.axis('off')
        
        plt.savefig(output_file)
        print(f"Graph saved to {output_file}")