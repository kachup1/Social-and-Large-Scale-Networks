import sys  # For command-line arguments
import networkx as nx  # Graph manipulation library
import matplotlib.pyplot as plt  # Plotting library
import numpy as np  # For numerical operations
from matplotlib.colors import LinearSegmentedColormap  # Color mapping

'''
SYNTAX TO RUN THE PROGRAM:

python ./graph_analysis.py graph_file.gml --components n --plot [C|N|P] --verify_homophily --verify_balanced_graph --output out_graph_file.gml

DESCRIPTION OF COMMANDS:

graph_file.gml                  : Input GML file representing the graph to analyze.
--components n                  : Partition the graph into n components (subgraphs/clusters).
--plot [C|N|P]                  : Plot the graph in different styles:
C                               : Clustering coefficient.
N                               : Neighborhood overlap.
P                               : Color nodes by attribute or default.
--verify_homophily              : Test for homophily in the graph (nodes with the same color are more likely to be connected).
--verify_balanced_graph         : Check if the graph is balanced based on edge signs.
--output out_graph_file.gml     : Save the updated graph with results to the specified output GML file.
'''
def plot_graph(graph, plot_style):
    # Get positions for nodes
    pos = nx.spring_layout(graph)
    
    if plot_style == 'C':  # Clustering coefficient
        clustering = nx.clustering(graph)  # Get clustering coefficients
        node_colors = [clustering[node] for node in graph.nodes()]
        nx.draw(graph, pos, node_color=node_colors, with_labels=True, cmap='Blues')
        
    elif plot_style == 'N':  # Neighborhood overlap
        # Placeholder for neighborhood overlap calculation
        node_colors = np.zeros(len(graph.nodes()))  # Replace with actual overlap calculation
        nx.draw(graph, pos, node_color=node_colors, with_labels=True, cmap='Reds')

    elif plot_style == 'P':  # Color nodes by attribute
        node_colors = apply_blue_to_magenta_colormap(graph)  # Use your existing color mapping
        nx.draw(graph, pos, node_color=node_colors, with_labels=True)
    
    plt.show()

def apply_blue_to_magenta_colormap(graph):
    colors = np.linspace(0, 1, len(graph.nodes()))  # Generate colors
    colormap = LinearSegmentedColormap.from_list("blue_magenta", ["blue", "magenta"])
    degrees = dict(graph.degree())  # Get node degrees
    max_degree = max(degrees.values())  # Find max degree
    # Map node degrees to colors
    node_colors = [colormap(degrees[node] / max_degree if max_degree > 0 else 0) for node in graph.nodes()]

    return node_colors  # Return list of node colors

def is_graph_balanced(graph):
    for cycle in nx.simple_cycles(graph):
        if len(cycle) % 2 == 1:  # If cycle length is odd
            # Count negative edges in the cycle
            negative_edges = sum(1 for u, v in zip(cycle, cycle[1:] + cycle[:1])
                                  if graph[u][v].get('sign', 1) == -1)
            if negative_edges % 2 == 1:  # If odd negative edges
                return False  # Not balanced
    return True  # Balanced

# Is balanced by node attributes
def is_graph_balanced_by_node_attributes(graph, attribute):
    for u, v, data in graph.edges(data=True):  # Get edges with data
        if attribute in graph.nodes[u] and attribute in graph.nodes[v]:
            node_u_attr = graph.nodes[u][attribute]  # Get node u's attribute
            node_v_attr = graph.nodes[v][attribute]  # Get node v's attribute
            if node_u_attr == node_v_attr:
                if data.get('sign', 1) != 1:  # Check sign
                    return False  # Not balanced
            else:
                if data.get('sign', 1) != -1:
                    return False
        else:
            return False  # One or both nodes lack attribute
    return True  # Balanced graph

def main():
    if len(sys.argv) < 2:  # Check for input graph file
        print("Error. Input invalid")
        sys.exit(1)  # Exit if not provided
    
    input_graph_file = sys.argv[1]
    plot_style = None
    verify_homophily = False
    verify_balanced_graph = False
    components = None

    # Manual parsing of command-line arguments
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '--plot':
            plot_style = sys.argv[i + 1]
        elif sys.argv[i] == '--verify_homophily':
            verify_homophily = True
        elif sys.argv[i] == '--verify_balanced_graph':
            verify_balanced_graph = True
        elif sys.argv[i] == '--components':
            components = int(sys.argv[i + 1])

    graph = nx.read_gml(input_graph_file)  # Load graph from GML file
    
    # Set edge signs based on color
    for u, v, data in graph.edges(data=True):
        # Red is -1, else +1
        data['sign'] = -1 if data.get('color') == 'r' else 1

    # Draw the graph if needed
    if verify_homophily or verify_balanced_graph:
        node_colors = apply_blue_to_magenta_colormap(graph)  # Get colors for nodes
        pos = nx.spring_layout(graph)  # Position nodes
        # Draw graph
        nx.draw(graph, pos, node_color=node_colors, with_labels=True)
        plt.show()

    if verify_balanced_graph:
        is_balanced = is_graph_balanced(graph)  # Check balance
        if is_balanced:
            print("The graph is balanced.")
        else:
            print("The graph is not balanced.")

    if verify_homophily:
        try:
            homophily_graph = nx.read_gml('homophily.gml')  # Load homophily graph
            color_map = {node: data['color'] for node, data in homophily_graph.nodes(data=True)}
            same_color_edges = 0  # Count same color edges
            different_color_edges = 0  # Count diff color edges
            # Check edges in graph
            for u, v in graph.edges():
                if color_map[u] == color_map[v]:  # If same color
                    same_color_edges += 1  # Increment count
                else:
                    different_color_edges += 1
            # Total edges
            total_edges = same_color_edges + different_color_edges
            if total_edges > 0:
                # Calculate proportion
                proportion_same_color = same_color_edges / total_edges
            else:
                print("Cannot determine homophily.")
        except FileNotFoundError:
            print("Error: homophily.gml file not found.")

    if components:
        while True:
            edge_betweenness = nx.edge_betweenness_centrality(graph)  # Get edge betweenness
            highest_edge = max(edge_betweenness, key=edge_betweenness.get)  # Find highest edge
            graph.remove_edge(*highest_edge)  # Remove highest edge
            components_list = list(nx.connected_components(graph))  # Get connected components
            num_components = len(components_list)
            if num_components >= components:
                break
        # Get colors for nodes
        node_colors = apply_blue_to_magenta_colormap(graph)
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, node_color=node_colors, with_labels=True)
        plt.show()

if __name__ == '__main__':
    main()
