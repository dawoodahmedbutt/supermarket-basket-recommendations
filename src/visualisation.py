import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualiser:
    def __init__(self, graph):
        self.graph_data = graph

    def plot_top_associations(self, min_weight=50, output_file="market_graph_global.png"):
        """Global co-purchase network — only edges above min_weight are shown."""
        G = nx.Graph()
        active_nodes = set()

        for node in self.graph_data.get_all_nodes():
            for neighbor, weight in self.graph_data.get_neighbors(node).items():
                if weight >= min_weight:
                    G.add_edge(node, neighbor, weight=weight)
                    active_nodes.update([node, neighbor])

        node_labels = {
            node: f"{node}\n({self.graph_data.get_node_frequency(node)})"
            for node in active_nodes
        }

        plt.figure(figsize=(14, 12))
        pos = nx.spring_layout(G, k=0.5, seed=42)

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
        """Star graph centred on one item, showing its top 15 strongest links."""
        G = nx.Graph()
        neighbors = self.graph_data.get_neighbors(center_node)

        if not neighbors:
            print(f"No neighbors found for {center_node}")
            return

        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)[:15]
        for neighbor, weight in sorted_neighbors:
            G.add_edge(center_node, neighbor, weight=weight)

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.6, seed=42)

        nx.draw_networkx_nodes(G, pos, nodelist=[center_node], node_size=3000, node_color='gold', edgecolors='black')
        neighbor_nodes = [n for n, w in sorted_neighbors]
        nx.draw_networkx_nodes(G, pos, nodelist=neighbor_nodes, node_size=1500, node_color='skyblue', alpha=0.9)

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
