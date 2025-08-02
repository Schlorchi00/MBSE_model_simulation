import collections

class Node:
    """Represents a single model in the network."""
    def __init__(self, node_id, domain, node_type, attributes=None, function_path=None):
        self.id = node_id
        self.domain = domain
        self.type = node_type
        self.attributes = attributes if attributes else {}
        self.function_path = function_path
        self.functionality_scores = collections.defaultdict(float)
        self.value_scores = collections.defaultdict(float)

    def __repr__(self):
        return f"Node({self.id})"

class WeightedEdge:
    """Defines a weighted connection for propagating scores (value or functionality)."""
    def __init__(self, source, target, label, weight):
        self.source = source
        self.target = target
        self.label = label
        self.weight = weight

class DependencyHyperedge:
    """Defines a workflow dependency: {A, B} -> C."""
    def __init__(self, sources, target):
        self.sources = set(sources)
        self.target = target