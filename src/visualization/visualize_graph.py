import hypernetx as hnx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_summary_graph(all_results):
    """
    Creates a final summary line chart comparing the meta and overall scores
    across all iterations.
    """
    iterations = [res['scenario_name'] for res in all_results]
    meta_scores = [res['meta_score'] for res in all_results]
    func_scores = [res['overall_scores']['Functionality'] for res in all_results]
    val_scores = [res['overall_scores']['Value'] for res in all_results]
    sus_scores = [res['overall_scores']['Sustainability'] for res in all_results]

    plt.figure(figsize=(15, 8))
    plt.plot(iterations, meta_scores, marker='o', linestyle='-', label='Meta Score (Overall)')
    plt.plot(iterations, func_scores, marker='s', linestyle='--', label='Overall Functionality')
    plt.plot(iterations, val_scores, marker='^', linestyle='--', label='Overall Value')
    plt.plot(iterations, sus_scores, marker='d', linestyle='--', label='Overall Sustainability')
    
    plt.title('Performance Across Design Iterations', fontsize=16)
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    
    filename = "final_summary_chart.png"
    plt.savefig(filename)
    print(f"\nSaved final summary chart to {filename}")
    plt.close()

# ... (plot_domain_scores and visualize_network_graph functions are the same as the previous version)
def plot_domain_scores(results, scenario_name):
    """
    Creates and saves a bar chart of specific Cost, Performance, and
    Sustainability scores for each domain.
    """
    key_metrics = ['total_cost', 'performance', 'sustainability']
    
    domain_scores = {
        'Material': {metric: [] for metric in key_metrics},
        'Design': {metric: [] for metric in key_metrics},
        'Manufacturing': {metric: [] for metric in key_metrics}
    }
    
    all_sustainability_scores = []

    # Aggregate specific scores from each node into its domain
    network = results['final_network']
    for node_id, state in results['node_states'].items():
        domain = network.get_node(node_id).domain
        if domain in domain_scores:
            all_scores = {**state['final_functionality_scores'], **state['final_value_scores']}
            for metric in key_metrics:
                if metric in all_scores:
                    domain_scores[domain][metric].append(all_scores[metric])
            if 'sustainability' in all_scores:
                all_sustainability_scores.append(all_scores['sustainability'])

    # Calculate the average score for each specific metric within each domain
    avg_scores = {domain: {} for domain in domain_scores}
    for domain, metrics in domain_scores.items():
        for metric, scores in metrics.items():
            avg_scores[domain][metric] = np.mean(scores) if scores else 0
            
    # Calculate overall sustainability
    overall_sustainability = np.mean(all_sustainability_scores) if all_sustainability_scores else 0
    
    # Create a DataFrame for easy plotting
    df = pd.DataFrame(avg_scores).T
    df.rename(columns={'total_cost': 'Cost', 'performance': 'Performance', 'sustainability': 'Sustainability'}, inplace=True)
    
    # Plotting
    ax = df.plot(kind='bar', figsize=(14, 8), rot=0, width=0.8)
    plt.title(f"Domain Scores for: {scenario_name}\nOverall Sustainability: {overall_sustainability:.3f}", fontsize=16)
    plt.ylabel("Average Score", fontsize=12)
    plt.xlabel("Domain", fontsize=12)
    plt.ylim(0, 1.1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Metrics')
    
    # Add score labels on top of bars
    for p in ax.patches:
        # Only add label if height is greater than 0
        if p.get_height() > 0:
            ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 9), textcoords='offset points', fontsize=9)

    # Save the plot to a file
    filename = f"detailed_scores_{scenario_name.replace(' ', '_')}.png"
    plt.tight_layout()
    plt.savefig(filename)
    print(f"  - Saved detailed scores plot to {filename}")
    plt.close()


def visualize_network_graph(network, scenario_name):
    """
    Creates and saves a visual hypergraph of the network using HyperNetX.
    """
    hypergraph_edges = {}
    for i, dep in enumerate(network.dependencies):
        hypergraph_edges[f"Dep-{i+1}"] = list(dep.sources) + [dep.target]
    for i, edge in enumerate(network.value_edges):
        hypergraph_edges[f"Value:{edge.label[:5]}-{i}"] = [edge.source, edge.target]
    for i, edge in enumerate(network.functionality_edges):
        hypergraph_edges[f"Func:{edge.label[:5]}-{i}"] = [edge.source, edge.target]

    H = hnx.Hypergraph(hypergraph_edges)
    
    domain_colors = {'Material': '#ff9999', 'Design': '#99ccff', 'Manufacturing': '#99ff99', 'Unknown': '#cccccc'}
    
    node_facecolors = {node_id: domain_colors.get(node_obj.domain, '#cccccc') for node_id, node_obj in network.nodes.items()}
    
    nodes_kwargs = {'facecolor': node_facecolors}

    plt.figure(figsize=(14, 10))
    hnx.draw(H, nodes_kwargs=nodes_kwargs, node_radius=0.6,
             node_labels_kwargs={'fontsize': 10, 'fontweight': 'bold'},
             edge_labels_kwargs={'fontsize': 9, 'alpha': 0.8, 'color': '#003366'})
    
    plt.title(f"Network Hypergraph for: {scenario_name}", size=16)
    
    # Save the plot to a file
    filename = f"network_{scenario_name.replace(' ', '_')}.png"
    plt.savefig(filename)
    print(f"  - Saved network graph to {filename}")
    plt.close()