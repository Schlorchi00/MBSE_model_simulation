import hypernetx as hnx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

def plot_summary_graph(all_results, summary_chart_path):
    """
    Creates a final summary line chart comparing the meta and overall scores
    across all iterations.
    """
    iterations = [res['scenario_name'] for res in all_results]
    meta_scores = [res['meta_score'] for res in all_results]
    func_scores = [res['overall_scores']['Functionality'] for res in all_results]
    val_scores = [res['overall_scores']['Value'] for res in all_results]
    sus_scores = [res['overall_scores']['Sustainability'] for res in all_results]

    # Adjusted figsize for a standard aspect ratio
    plt.figure(figsize=(11, 6.5))
    plt.plot(iterations, meta_scores, marker='o', linestyle='-', label='Meta Score (Overall)')
    plt.plot(iterations, func_scores, marker='s', linestyle='--', label='Overall Functionality')
    plt.plot(iterations, val_scores, marker='^', linestyle='--', label='Overall Value')
    plt.plot(iterations, sus_scores, marker='d', linestyle='--', label='Overall Sustainability')
    
    plt.title('Performance Across Design Scenarios', fontsize=16)
    plt.xlabel('Scenario', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    
    # Save with specific DPI and tight bounding box for consistent sizing
    plt.savefig(summary_chart_path, dpi=150, bbox_inches='tight')
    print(f"\nSaved final summary chart to {summary_chart_path}")
    plt.close()

def plot_domain_scores(results, scenario_name):
    """
    Creates and saves a stacked bar chart showing the contribution of each node
    to the key metrics within each domain, identifying hotspots.
    """
    key_metrics = {
        'total_cost': 'Cost',
        'performance': 'Performance',
        'sustainability': 'Sustainability'
    }
    
    records = []
    network = results['final_network']

    for node_id, state in results['node_states'].items():
        domain = network.get_node(node_id).domain
        all_scores = {**state['final_functionality_scores'], **state['final_value_scores']}
        for metric_key, metric_name in key_metrics.items():
            if metric_key in all_scores:
                records.append({
                    'domain': domain,
                    'node': node_id,
                    'metric': metric_name,
                    'score': all_scores[metric_key]
                })

    if not records:
        print("  - No data to plot for domain scores.")
        return

    df = pd.DataFrame(records)

    # --- FIX: Adjusted figsize and removed suptitle ---
    fig, axes = plt.subplots(len(key_metrics), 1, figsize=(8, 9), sharex=True)
    # fig.suptitle(f"Domain Hotspots for: {scenario_name}", fontsize=18, y=0.98) # Removed header

    for i, metric_name in enumerate(key_metrics.values()):
        ax = axes[i]
        metric_df = df[df['metric'] == metric_name]
        
        if metric_df.empty:
            ax.set_title(f"{metric_name} Scores by Domain")
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax.transAxes)
            continue

        pivot_df = metric_df.pivot_table(index='domain', columns='node', values='score', aggfunc='sum').fillna(0)
        pivot_df.plot(kind='bar', stacked=True, ax=ax, rot=0, width=0.8)
        
        ax.set_title(f"{metric_name} Scores by Domain")
        ax.set_ylabel("Aggregated Score")
        ax.legend(title='Contributing Models', bbox_to_anchor=(1.04, 1), loc="upper left")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.xlabel("Domain", fontsize=12)
    plt.tight_layout(rect=[0, 0, 0.85, 1.0]) # Adjust layout

    filename = f"detailed_scores_{scenario_name}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"  - Saved detailed scores plot to {filename}")
    plt.close()


def visualize_network_graph(network, scenario_name):
    """
    Creates and saves a visual hypergraph of the network using HyperNetX,
    including a detailed legend and a table of weighted connections.
    """
    fig = plt.figure(figsize=(10, 12))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.5])
    ax_graph = fig.add_subplot(gs[0])
    ax_table = fig.add_subplot(gs[1])

    hypergraph_edges = {}
    for i, dep in enumerate(network.dependencies):
        hypergraph_edges[f"Dep-{i+1}"] = list(dep.sources) + [dep.target]
    
    simple_edges_data = []
    for edge in network.value_edges:
        hypergraph_edges[f"V:{edge.label[:4]}-{edge.source[:4]}"] = [edge.source, edge.target]
        simple_edges_data.append(['Value', edge.source, edge.target, edge.label, f"{edge.weight:.2f}"])
    for edge in network.functionality_edges:
        hypergraph_edges[f"F:{edge.label[:4]}-{edge.source[:4]}"] = [edge.source, edge.target]
        simple_edges_data.append(['Functionality', edge.source, edge.target, edge.label, f"{edge.weight:.2f}"])

    H = hnx.Hypergraph(hypergraph_edges)
    
    domain_colors = {'Material': '#ff9999', 'Design': '#99ccff', 'Manufacturing': '#99ff99', 'Unknown': '#cccccc'}
    node_facecolors = {node_id: domain_colors.get(node_obj.domain, '#cccccc') for node_id, node_obj in network.nodes.items()}
    nodes_kwargs = {'facecolor': node_facecolors}

    hnx.draw(H, ax=ax_graph, nodes_kwargs=nodes_kwargs, node_radius=0.6,
             node_labels_kwargs={'fontsize': 9, 'fontweight': 'bold'},
             edge_labels_kwargs={'fontsize': 8, 'alpha': 0.8, 'color': '#003366'})
    
    legend_handles = [
        mpatches.Patch(color=domain_colors['Material'], label='Material Domain'),
        mpatches.Patch(color=domain_colors['Design'], label='Design Domain'),
        mpatches.Patch(color=domain_colors['Manufacturing'], label='Manufacturing Domain'),
        plt.Line2D([0], [0], marker='o', color='w', label='Model Node', markerfacecolor='grey', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Dependency Hyperedge', markerfacecolor='#ffcc66', markersize=10)
    ]
    ax_graph.legend(handles=legend_handles, title="Legend", loc='upper left', bbox_to_anchor=(1.01, 1.0))
    ax_graph.set_title(f"Network Hypergraph for: {scenario_name}", size=16)

    ax_table.axis('off')
    ax_table.set_title('Weighted Connections', size=14)
    if simple_edges_data:
        df = pd.DataFrame(simple_edges_data, columns=['Type', 'Source', 'Target', 'Label', 'Weight'])
        
        # --- FIX: Manually set column widths and font size ---
        col_widths = [0.2, 0.25, 0.25, 0.2, 0.1]
        table = ax_table.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left', colWidths=col_widths)
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2) # Adjust vertical scaling
    else:
        ax_table.text(0.5, 0.5, 'No weighted connections.', ha='center', va='center')

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    filename = f"network_{scenario_name}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"  - Saved network graph to {filename}")
    plt.close()