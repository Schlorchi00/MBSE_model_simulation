from .graph_components import Node, WeightedEdge, DependencyHyperedge

class DynamicNetwork:
    """Manages the overall graph structure."""
    def __init__(self):
        self.nodes = {}
        self.value_edges = []
        self.functionality_edges = []
        self.dependencies = []

    def add_node(self, node):
        self.nodes[node.id] = node

    def load_from_config(self, config_data):
        """
        Builds the network from a scenario dictionary with robust, multi-pass logic.
        """
        print("--- Loading Network Configuration ---")
        # 1. Discover ALL nodes that will be in the graph, from both 'nodes' and 'edges' lists.
        all_node_ids = set()
        for node_data in config_data.get('nodes', []):
            all_node_ids.add(node_data['node_id'])
        for edge_data in config_data.get('edges', []):
            if 'source' in edge_data: all_node_ids.add(edge_data['source'])
            if 'sources' in edge_data: all_node_ids.update(edge_data['sources'])
            if 'target' in edge_data: all_node_ids.add(edge_data['target'])

        # 2. Create all Node objects based on the discovered set.
        print("Step 1: Creating all nodes...")
        for node_id in sorted(list(all_node_ids)): # Sorting for deterministic order
            # Find this node's specific data in the config, if it exists.
            node_data = next((n for n in config_data.get('nodes', []) if n['node_id'] == node_id), None)
            if node_data:
                print(f"  - Adding defined node: {node_id}")
                self.add_node(Node(**node_data))
            else:
                # If a node is only mentioned in an edge, create a default object for it.
                print(f"  - Creating default node for implicit node: {node_id}")
                self.add_node(Node(node_id=node_id, domain='Unknown', node_type='Unknown'))
        
        # 3. Now that all nodes exist, load the edges.
        print("\nStep 2: Loading edges...")
        for edge_data in config_data.get('edges', []):
            edge_info = edge_data.copy()
            edge_type = edge_info.pop('type')
            
            if edge_type == 'dependency':
                self.dependencies.append(DependencyHyperedge(**edge_info))
            elif edge_type == 'value':
                self.value_edges.append(WeightedEdge(**edge_info))
            elif edge_type == 'functionality':
                self.functionality_edges.append(WeightedEdge(**edge_info))
        print("--- Network Loading Complete ---\n")

    def get_node(self, node_id):
        return self.nodes.get(node_id)