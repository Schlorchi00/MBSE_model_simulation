import hypernetx as hnx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import seaborn as sns

def plot_weighting_impact(all_results, output_path):
    """
    Creates a grouped bar chart showing the impact of different weighting
    strategies on the final overall scores.
    """
    records = []
    for res in all_results:
        parts = res['scenario_name'].split('_')
        weight_strategy = parts[-1]
        base_design = "_".join(parts[:-1])
        
        records.append({
            'Base Design': base_design,
            'Weighting Strategy': weight_strategy,
            'Meta Score': res['meta_score']
        })
    
    df = pd.DataFrame(records)
    pivot_df = df.pivot_table(index='Base Design', columns='Weighting Strategy', values='Meta Score', aggfunc='mean')
    
    ordered_cols = [col for col in ['Balanced', 'Cost-Focused', 'Sustain-Focused', 'Perf-Focused'] if col in pivot_df.columns]
    pivot_df = pivot_df[ordered_cols]
    
    ax = pivot_df.plot(kind='bar', figsize=(14, 8), rot=45)
    plt.title('Impact of Weighting Strategies on Meta Score', fontsize=16)
    plt.ylabel('Final Meta Score', fontsize=12)
    plt.xlabel('Base Design Scenario', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Weighting Strategy')
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 9), textcoords='offset points', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nSaved weighting impact summary chart to {output_path}")
    plt.close()

def plot_base_design_comparison(base_design_results, output_path):
    """
    Creates a bar chart comparing the meta-scores of each base design.
    """
    records = []
    for res in base_design_results:
        records.append({
            'Scenario': res['scenario_name'],
            'Meta Score': res['meta_score'],
            'Functionality': res['overall_scores']['Functionality'],
            'Value': res['overall_scores']['Value'],
            'Sustainability': res['overall_scores']['Sustainability']
        })
    
    df = pd.DataFrame(records)
    df.set_index('Scenario', inplace=True)
    
    ax = df.plot(kind='bar', figsize=(12, 7), rot=45)
    plt.title('Overall Score Comparison Across Base Designs (Balanced Weights)', fontsize=16)
    plt.ylabel('Average Score', fontsize=12)
    plt.xlabel('Design Scenario', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 9), textcoords='offset points', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nSaved final summary comparison chart to {output_path}")
    plt.close()

# ... (rest of the file is the same)
def plot_domain_scores(results, scenario_name):
    key_metrics = {'total_cost': 'Cost', 'performance': 'Performance', 'sustainability': 'Sustainability'}
    records = []
    network = results['final_network']
    for node_id, state in results['node_states'].items():
        domain = network.get_node(node_id).domain
        all_scores = {**state['final_functionality_scores'], **state['final_value_scores']}
        for metric_key, metric_name in key_metrics.items():
            if metric_key in all_scores:
                records.append({'domain': domain, 'node': node_id, 'metric': metric_name, 'score': all_scores[metric_key]})
    if not records:
        print("  - No data to plot for domain scores.")
        return
    df = pd.DataFrame(records)
    fig, axes = plt.subplots(len(key_metrics), 1, figsize=(8, 9), sharex=True)
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
    plt.tight_layout(rect=[0, 0, 0.85, 1.0])
    filename = f"detailed_scores_{scenario_name}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"  - Saved detailed scores plot to {filename}")
    plt.close()

def visualize_network_graph(network, scenario_name):
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
    legend_handles = [mpatches.Patch(color=domain_colors['Material'], label='Material Domain'), mpatches.Patch(color=domain_colors['Design'], label='Design Domain'), mpatches.Patch(color=domain_colors['Manufacturing'], label='Manufacturing Domain'), plt.Line2D([0], [0], marker='o', color='w', label='Model Node', markerfacecolor='grey', markersize=10), plt.Line2D([0], [0], marker='s', color='w', label='Dependency Hyperedge', markerfacecolor='#ffcc66', markersize=10)]
    ax_graph.legend(handles=legend_handles, title="Legend", loc='upper left', bbox_to_anchor=(1.01, 1.0))
    ax_graph.set_title(f"Network Hypergraph for: {scenario_name}", size=16)
    ax_table.axis('off')
    ax_table.set_title('Weighted Connections', size=14)
    if simple_edges_data:
        df = pd.DataFrame(simple_edges_data, columns=['Type', 'Source', 'Target', 'Label', 'Weight'])
        col_widths = [0.2, 0.25, 0.25, 0.2, 0.1]
        table = ax_table.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left', colWidths=col_widths)
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2)
    else:
        ax_table.text(0.5, 0.5, 'No weighted connections.', ha='center', va='center')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    filename = f"network_{scenario_name}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"  - Saved network graph to {filename}")
    plt.close()