"""
Graph Data Structure Implementation
Lab Assignment: Become familiar with the graph data structure and its applications.

A Graph G(V, E) is a non-empty finite set V of elements called vertices
together with a possibly empty set E of pairs of vertices called edges.
"""

from collections import deque


class Graph:
    """
    Graph data structure implemented using an adjacency list.

    Supports both directed and undirected graphs.
    Vertices can be any hashable value (int, str, etc.).
    """

    def __init__(self, directed=False):
        """
        Initialize an empty graph.

        Args:
            directed (bool): If True, the graph is directed (digraph).
                             If False (default), the graph is undirected.
        """
        self._adjacency_list = {}  # dict mapping vertex -> set of neighbours
        self._directed = directed

    # ------------------------------------------------------------------
    # Basic properties
    # ------------------------------------------------------------------

    @property
    def vertices(self):
        """Return the set of all vertices in the graph."""
        return set(self._adjacency_list.keys())

    @property
    def edges(self):
        """
        Return the set of all edges in the graph.

        For undirected graphs each edge (u, v) appears only once
        (with u <= v when comparable, otherwise in insertion order).
        For directed graphs each (u, v) is a directed edge from u to v.
        """
        edge_set = set()
        for vertex, neighbours in self._adjacency_list.items():
            for neighbour in neighbours:
                if self._directed:
                    edge_set.add((vertex, neighbour))
                else:
                    # Avoid duplicate (u,v) and (v,u) for undirected graphs
                    edge = tuple(sorted([vertex, neighbour], key=str))
                    edge_set.add(edge)
        return edge_set

    @property
    def is_directed(self):
        """Return True if the graph is directed."""
        return self._directed

    def vertex_count(self):
        """Return the number of vertices."""
        return len(self._adjacency_list)

    def edge_count(self):
        """Return the number of edges."""
        return len(self.edges)

    # ------------------------------------------------------------------
    # Vertex operations
    # ------------------------------------------------------------------

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.

        Args:
            vertex: The vertex to add (must be hashable).

        Raises:
            ValueError: If the vertex already exists.
        """
        if vertex in self._adjacency_list:
            raise ValueError(f"Vertex '{vertex}' already exists in the graph.")
        self._adjacency_list[vertex] = set()

    def remove_vertex(self, vertex):
        """
        Remove a vertex and all its incident edges from the graph.

        Args:
            vertex: The vertex to remove.

        Raises:
            ValueError: If the vertex does not exist.
        """
        if vertex not in self._adjacency_list:
            raise ValueError(f"Vertex '{vertex}' does not exist in the graph.")

        # Remove all edges pointing TO this vertex
        for v in self._adjacency_list:
            self._adjacency_list[v].discard(vertex)

        # Remove the vertex itself (and its outgoing edges)
        del self._adjacency_list[vertex]

    def has_vertex(self, vertex):
        """Return True if the vertex exists in the graph."""
        return vertex in self._adjacency_list

    # ------------------------------------------------------------------
    # Edge operations
    # ------------------------------------------------------------------

    def add_edge(self, source, destination):
        """
        Add an edge between source and destination.

        For undirected graphs this adds edges in both directions.
        Missing vertices are created automatically.

        Args:
            source:      The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If the edge already exists.
        """
        # Auto-create vertices if they don't exist
        if source not in self._adjacency_list:
            self.add_vertex(source)
        if destination not in self._adjacency_list:
            self.add_vertex(destination)

        if destination in self._adjacency_list[source]:
            raise ValueError(
                f"Edge from '{source}' to '{destination}' already exists."
            )

        self._adjacency_list[source].add(destination)
        if not self._directed:
            self._adjacency_list[destination].add(source)

    def remove_edge(self, source, destination):
        """
        Remove the edge between source and destination.

        Args:
            source:      The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If either vertex or the edge does not exist.
        """
        if source not in self._adjacency_list:
            raise ValueError(f"Vertex '{source}' does not exist in the graph.")
        if destination not in self._adjacency_list:
            raise ValueError(f"Vertex '{destination}' does not exist in the graph.")
        if destination not in self._adjacency_list[source]:
            raise ValueError(
                f"Edge from '{source}' to '{destination}' does not exist."
            )

        self._adjacency_list[source].discard(destination)
        if not self._directed:
            self._adjacency_list[destination].discard(source)

    def has_edge(self, source, destination):
        """Return True if an edge from source to destination exists."""
        return (
            source in self._adjacency_list
            and destination in self._adjacency_list[source]
        )

    def get_neighbours(self, vertex):
        """
        Return the set of neighbours (adjacent vertices) of a vertex.

        Args:
            vertex: The vertex whose neighbours are requested.

        Raises:
            ValueError: If the vertex does not exist.
        """
        if vertex not in self._adjacency_list:
            raise ValueError(f"Vertex '{vertex}' does not exist in the graph.")
        return set(self._adjacency_list[vertex])

    # ------------------------------------------------------------------
    # Graph traversals
    # ------------------------------------------------------------------

    def bfs(self, start):
        """
        Breadth-First Search starting from *start*.

        Returns a list of vertices in the order they are visited.

        Args:
            start: The starting vertex.

        Raises:
            ValueError: If the start vertex does not exist.
        """
        if start not in self._adjacency_list:
            raise ValueError(f"Vertex '{start}' does not exist in the graph.")

        visited = []
        seen = set()
        queue = deque([start])
        seen.add(start)

        while queue:
            vertex = queue.popleft()
            visited.append(vertex)
            for neighbour in sorted(self._adjacency_list[vertex], key=str):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)

        return visited

    def dfs(self, start):
        """
        Depth-First Search starting from *start*.

        Returns a list of vertices in the order they are visited.

        Args:
            start: The starting vertex.

        Raises:
            ValueError: If the start vertex does not exist.
        """
        if start not in self._adjacency_list:
            raise ValueError(f"Vertex '{start}' does not exist in the graph.")

        visited = []
        seen = set()

        def _dfs_recursive(vertex):
            seen.add(vertex)
            visited.append(vertex)
            for neighbour in sorted(self._adjacency_list[vertex], key=str):
                if neighbour not in seen:
                    _dfs_recursive(neighbour)

        _dfs_recursive(start)
        return visited

    # ------------------------------------------------------------------
    # Path / connectivity helpers
    # ------------------------------------------------------------------

    def has_path(self, source, destination):
        """
        Return True if there is a path from source to destination.

        Uses BFS internally.

        Args:
            source:      The source vertex.
            destination: The destination vertex.

        Raises:
            ValueError: If either vertex does not exist.
        """
        if source not in self._adjacency_list:
            raise ValueError(f"Vertex '{source}' does not exist in the graph.")
        if destination not in self._adjacency_list:
            raise ValueError(f"Vertex '{destination}' does not exist in the graph.")

        return destination in self.bfs(source)

    def is_connected(self):
        """
        Return True if the graph is connected (undirected) or
        strongly connected (directed — every vertex can reach every other).

        Returns False for an empty graph.
        """
        if not self._adjacency_list:
            return False

        vertices = list(self._adjacency_list.keys())

        if not self._directed:
            # Undirected: BFS/DFS from any vertex should visit all vertices
            return set(self.bfs(vertices[0])) == set(vertices)

        # Directed: check that every vertex can reach every other vertex
        for v in vertices:
            if set(self.bfs(v)) != set(vertices):
                return False
        return True

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display(self):
        """Print the adjacency list of the graph."""
        graph_type = "Directed" if self._directed else "Undirected"
        print(f"Graph ({graph_type})")
        print(f"  Vertices ({self.vertex_count()}): {sorted(self.vertices, key=str)}")
        print(f"  Edges    ({self.edge_count()}):")
        for vertex in sorted(self._adjacency_list.keys(), key=str):
            neighbours = sorted(self._adjacency_list[vertex], key=str)
            print(f"    {vertex} -> {neighbours}")

    def __repr__(self):
        graph_type = "directed" if self._directed else "undirected"
        return (
            f"Graph({graph_type}, "
            f"vertices={self.vertex_count()}, "
            f"edges={self.edge_count()})"
        )
