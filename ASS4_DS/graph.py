class Graph:
    """Graph class supporting directed and undirected graphs"""
    
    def __init__(self, nodes):
        """
        Initialize graph
        
        Args:
            nodes: List of nodes or integer for range of nodes
        """
        if isinstance(nodes, int):
            self.nodes = list(range(nodes))
            self.vertices = nodes
        else:
            self.nodes = nodes
            self.vertices = len(nodes)
        
        self.adj = {node: [] for node in self.nodes}
        self.graph_type = None

    def add_edge_directed(self, u, v, weight=None):
        """Add directed edge from u to v"""
        if u not in self.nodes or v not in self.nodes:
            raise ValueError(f"Node must be in {self.nodes}")
        
        if weight is not None:
            self.adj[u].append((v, weight))
        else:
            self.adj[u].append(v)
        
        self.graph_type = 'directed'

    def add_edge_undirected(self, u, v, weight=None):
        """Add undirected edge between u and v"""
        if u not in self.nodes or v not in self.nodes:
            raise ValueError(f"Node must be in {self.nodes}")
        
        if weight is not None:
            self.adj[u].append((v, weight))
            self.adj[v].append((u, weight))
        else:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.graph_type = 'undirected'

    def get_in_degree(self, node):
        """Calculate in-degree of node (number of incoming edges)"""
        count = 0
        for u in self.adj:
            neighbors = self.adj[u]
            for neighbor in neighbors:
                if isinstance(neighbor, tuple):
                    if neighbor[0] == node:
                        count += 1
                else:
                    if neighbor == node:
                        count += 1
        return count

    def get_out_degree(self, node):
        """Calculate out-degree of node (number of outgoing edges)"""
        neighbors = self.adj[node]
        return len(neighbors)

    def get_all_in_degrees(self):
        """Get in-degrees of all nodes"""
        return {node: self.get_in_degree(node) for node in self.nodes}

    def print_graph(self):
        """Print the graph"""
        print("\n" + "="*50)
        print(f"Graph ({self.graph_type}): {self.vertices} nodes, {self.count_edges()} edges")
        print("="*50)
        for node in self.nodes:
            print(f"{node} -> {self.adj[node]}")
        print("="*50 + "\n")

    def count_edges(self):
        """Count total edges"""
        count = 0
        for neighbors in self.adj.values():
            count += len(neighbors)
        
        if self.graph_type == 'undirected':
            count = count // 2
        
        return count

    def to_dict(self):
        """Convert graph to dictionary for visualization"""
        return dict(self.adj)

    def validate(self):
        """Validate graph structure"""
        for u in self.adj:
            if u not in self.nodes:
                return False, f"Node {u} not in nodes list"
            
            for neighbor in self.adj[u]:
                v = neighbor[0] if isinstance(neighbor, tuple) else neighbor
                if v not in self.nodes:
                    return False, f"Invalid edge: {u} -> {v}"
        
        return True, "Graph is valid"
