import hypernetx as hnx
import matplotlib.pyplot as plt

def visualize_network_graph(network, scenario_name):
    """
    Creates and displays a visual hypergraph of the network using HyperNetX.
    """
    hypergraph_edges = {}

    # 1. Add dependency hyperedges
    for i, dep in enumerate(network.dependencies):
        edge_id = f"Dep-{i+1}"
        hypergraph_edges[edge_id] = list(dep.sources) + [dep.target]

    # 2. Add pairwise value edges (with unique IDs)
    for i, edge in enumerate(network.value_edges):
        edge_id = f"Value: {edge.label[:5]}-{i}"
        hypergraph_edges[edge_id] = [edge.source, edge.target]

    # 3. Add pairwise functionality edges (with unique IDs)
    for i, edge in enumerate(network.functionality_edges):
        edge_id = f"Func: {edge.label[:5]}-{i}"
        hypergraph_edges[edge_id] = [edge.source, edge.target]

    H = hnx.Hypergraph(hypergraph_edges)

    # Define colors for each domain for clear visual grouping
    domain_colors = {
        'Material': '#ff9999',
        'Design': '#99ccff',
        'Manufacturing': '#99ff99',
        'Unknown': '#cccccc'
    }

    # --- FIX: Restructure the kwargs to the format HyperNetX expects ---
    # It should be {'style_property': {'node1': value1, 'node2': value2}}
    node_facecolors = {
        node_id: domain_colors.get(node_obj.domain, '#cccccc')
        for node_id, node_obj in network.nodes.items()
    }
    
    nodes_kwargs = {
        'facecolor': node_facecolors
    }

    # --- Plotting ---
    plt.figure(figsize=(14, 10))
    
    hnx.draw(H,
             nodes_kwargs=nodes_kwargs,
             node_radius=0.6,
             node_labels_kwargs={'fontsize': 10, 'fontweight': 'bold'},
             edge_labels_kwargs={'fontsize': 9, 'alpha': 0.8, 'color': '#003366'}
            )
    
    plt.title(f"Hypergraph Visualization for: {scenario_name}", size=16)
    plt.show()