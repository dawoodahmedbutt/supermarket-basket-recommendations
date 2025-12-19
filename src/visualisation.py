import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualiser:
    def __init__(self, graph):
        self.graph_data = graph

    def plot_top_associations(self, min_weight=50, output_file="market_graph_global.png"):
        """
        Plots the graph with Node Counts and Edge Weights.
        """
        G = nx.Graph()

        # Build NetworkX graph
        nodes = self.graph_data.get_all_nodes()
        active_nodes = set()

        for node in nodes:
            neighbors = self.graph_data.get_neighbors(node)
            for neighbor, weight in neighbors.items():
                if weight >= min_weight:
                    G.add_edge(node, neighbor, weight=weight)
                    active_nodes.add(node)
                    active_nodes.add(neighbor)

        # Setup Labels 
        node_labels = {}
        for node in active_nodes:
            count = self.graph_data.get_node_frequency(node)
            node_labels[node] = f"{node}\n({count})"

        # Setup Plot
        plt.figure(figsize=(14, 12)) 
        
        pos = nx.spring_layout(G, k=0.5, seed=42)

        # Draw
        nx.draw_networkx_nodes(G, pos, node_size=2500, node_color='lightgreen', alpha=0.9)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9, font_family='sans-serif', font_weight='bold')
        
        edges = G.edges(data=True)
        widths = [data['weight'] * 0.02 for _, _, data in edges]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color='gray', alpha=0.4)
        
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

        plt.title(f"Supermarket Network (Strong Links > {min_weight} Transactions)", fontsize=16)
        plt.axis('off')
        
        plt.savefig(output_file)
        plt.close() 
        print(f"Graph saved to {output_file}")

    def plot_ego_graph(self, center_node, output_file):
        """
        Plots a 'Star Graph' focusing on one central item and its connections.
        """
        G = nx.Graph()
        
        # Get neighbors of the center node
        neighbors = self.graph_data.get_neighbors(center_node)
        
        if not neighbors:
            print(f"No neighbors found for {center_node}")
            return

        # Filter: Only keep the top 15 strongest links
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)[:15]
        
        for neighbor, weight in sorted_neighbors:
            G.add_edge(center_node, neighbor, weight=weight)

        # Setup Layout (Star Layout)
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.6, seed=42)
        
        # Draw Center Node (Gold color)
        nx.draw_networkx_nodes(G, pos, nodelist=[center_node], node_size=3000, node_color='gold', edgecolors='black')
        
        # Draw Neighbors (Blue color)
        neighbor_nodes = [n for n, w in sorted_neighbors]
        nx.draw_networkx_nodes(G, pos, nodelist=neighbor_nodes, node_size=1500, node_color='skyblue', alpha=0.9)
        
        # Labels & Edges
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        edges = G.edges(data=True)
        widths = [data['weight'] * 0.05 for _, _, data in edges]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color='gray', alpha=0.5)
        
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title(f"Ego Network: {center_node}", fontsize=14)
        plt.axis('off')
        
        plt.savefig(output_file)
        plt.close() 
