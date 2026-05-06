"""
Tests for the Graph data structure implementation.
"""

import pytest
from graph import Graph


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def undirected_graph():
    """Return a simple undirected graph for reuse across tests."""
    g = Graph(directed=False)
    for v in ["A", "B", "C", "D", "E"]:
        g.add_vertex(v)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")
    return g


@pytest.fixture
def directed_graph():
    """Return a simple directed graph for reuse across tests."""
    g = Graph(directed=True)
    for v in [1, 2, 3, 4]:
        g.add_vertex(v)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 4)
    return g


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

class TestInit:
    def test_empty_undirected_graph(self):
        g = Graph()
        assert g.vertex_count() == 0
        assert g.edge_count() == 0
        assert not g.is_directed

    def test_empty_directed_graph(self):
        g = Graph(directed=True)
        assert g.vertex_count() == 0
        assert g.edge_count() == 0
        assert g.is_directed

    def test_repr(self):
        g = Graph()
        assert "undirected" in repr(g)
        g2 = Graph(directed=True)
        assert "directed" in repr(g2)


# ---------------------------------------------------------------------------
# Vertex operations
# ---------------------------------------------------------------------------

class TestVertexOperations:
    def test_add_vertex(self):
        g = Graph()
        g.add_vertex(1)
        assert g.has_vertex(1)
        assert g.vertex_count() == 1

    def test_add_multiple_vertices(self):
        g = Graph()
        for v in range(5):
            g.add_vertex(v)
        assert g.vertex_count() == 5
        assert g.vertices == {0, 1, 2, 3, 4}

    def test_add_duplicate_vertex_raises(self):
        g = Graph()
        g.add_vertex("X")
        with pytest.raises(ValueError):
            g.add_vertex("X")

    def test_remove_vertex(self, undirected_graph):
        undirected_graph.remove_vertex("E")
        assert not undirected_graph.has_vertex("E")
        assert undirected_graph.vertex_count() == 4

    def test_remove_vertex_removes_incident_edges(self, undirected_graph):
        undirected_graph.remove_vertex("D")
        # Edges to/from D should be gone
        assert not undirected_graph.has_edge("B", "D")
        assert not undirected_graph.has_edge("C", "D")

    def test_remove_nonexistent_vertex_raises(self):
        g = Graph()
        with pytest.raises(ValueError):
            g.remove_vertex("Z")

    def test_has_vertex_false(self):
        g = Graph()
        assert not g.has_vertex(99)


# ---------------------------------------------------------------------------
# Edge operations
# ---------------------------------------------------------------------------

class TestEdgeOperations:
    def test_add_edge_undirected(self):
        g = Graph()
        g.add_edge(1, 2)
        assert g.has_edge(1, 2)
        assert g.has_edge(2, 1)  # undirected: both directions

    def test_add_edge_directed(self):
        g = Graph(directed=True)
        g.add_edge(1, 2)
        assert g.has_edge(1, 2)
        assert not g.has_edge(2, 1)  # directed: only one direction

    def test_add_edge_auto_creates_vertices(self):
        g = Graph()
        g.add_edge("X", "Y")
        assert g.has_vertex("X")
        assert g.has_vertex("Y")

    def test_add_duplicate_edge_raises(self):
        g = Graph()
        g.add_edge(1, 2)
        with pytest.raises(ValueError):
            g.add_edge(1, 2)

    def test_remove_edge_undirected(self, undirected_graph):
        undirected_graph.remove_edge("A", "B")
        assert not undirected_graph.has_edge("A", "B")
        assert not undirected_graph.has_edge("B", "A")

    def test_remove_edge_directed(self, directed_graph):
        directed_graph.remove_edge(1, 2)
        assert not directed_graph.has_edge(1, 2)
        # Other edges should be unaffected
        assert directed_graph.has_edge(1, 3)

    def test_remove_nonexistent_edge_raises(self):
        g = Graph()
        g.add_vertex(1)
        g.add_vertex(2)
        with pytest.raises(ValueError):
            g.remove_edge(1, 2)

    def test_remove_edge_missing_vertex_raises(self):
        g = Graph()
        g.add_vertex(1)
        with pytest.raises(ValueError):
            g.remove_edge(1, 99)

    def test_get_neighbours(self, undirected_graph):
        assert undirected_graph.get_neighbours("A") == {"B", "C"}

    def test_get_neighbours_directed(self, directed_graph):
        assert directed_graph.get_neighbours(1) == {2, 3}
        assert directed_graph.get_neighbours(2) == {4}

    def test_get_neighbours_nonexistent_raises(self):
        g = Graph()
        with pytest.raises(ValueError):
            g.get_neighbours(42)

    def test_edge_count_undirected(self, undirected_graph):
        assert undirected_graph.edge_count() == 5

    def test_edge_count_directed(self, directed_graph):
        assert directed_graph.edge_count() == 4


# ---------------------------------------------------------------------------
# Traversals
# ---------------------------------------------------------------------------

class TestBFS:
    def test_bfs_visits_all_connected_vertices(self, undirected_graph):
        result = undirected_graph.bfs("A")
        assert set(result) == {"A", "B", "C", "D", "E"}

    def test_bfs_start_is_first(self, undirected_graph):
        result = undirected_graph.bfs("A")
        assert result[0] == "A"

    def test_bfs_single_vertex(self):
        g = Graph()
        g.add_vertex(1)
        assert g.bfs(1) == [1]

    def test_bfs_directed(self, directed_graph):
        result = directed_graph.bfs(1)
        assert result[0] == 1
        assert set(result) == {1, 2, 3, 4}

    def test_bfs_nonexistent_start_raises(self):
        g = Graph()
        with pytest.raises(ValueError):
            g.bfs(99)


class TestDFS:
    def test_dfs_visits_all_connected_vertices(self, undirected_graph):
        result = undirected_graph.dfs("A")
        assert set(result) == {"A", "B", "C", "D", "E"}

    def test_dfs_start_is_first(self, undirected_graph):
        result = undirected_graph.dfs("A")
        assert result[0] == "A"

    def test_dfs_single_vertex(self):
        g = Graph()
        g.add_vertex(1)
        assert g.dfs(1) == [1]

    def test_dfs_directed(self, directed_graph):
        result = directed_graph.dfs(1)
        assert result[0] == 1
        assert set(result) == {1, 2, 3, 4}

    def test_dfs_nonexistent_start_raises(self):
        g = Graph()
        with pytest.raises(ValueError):
            g.dfs(99)


# ---------------------------------------------------------------------------
# Path and connectivity
# ---------------------------------------------------------------------------

class TestPathAndConnectivity:
    def test_has_path_true(self, undirected_graph):
        assert undirected_graph.has_path("A", "E")

    def test_has_path_false(self):
        g = Graph()
        g.add_vertex("X")
        g.add_vertex("Y")
        # No edge between X and Y
        assert not g.has_path("X", "Y")

    def test_has_path_same_vertex(self, undirected_graph):
        assert undirected_graph.has_path("A", "A")

    def test_has_path_directed(self, directed_graph):
        assert directed_graph.has_path(1, 4)
        # In a directed graph, 4 cannot reach 1
        assert not directed_graph.has_path(4, 1)

    def test_has_path_nonexistent_raises(self):
        g = Graph()
        g.add_vertex(1)
        with pytest.raises(ValueError):
            g.has_path(1, 99)

    def test_is_connected_undirected_true(self, undirected_graph):
        assert undirected_graph.is_connected()

    def test_is_connected_undirected_false(self):
        g = Graph()
        g.add_vertex(1)
        g.add_vertex(2)
        # Two isolated vertices — not connected
        assert not g.is_connected()

    def test_is_connected_empty_graph(self):
        g = Graph()
        assert not g.is_connected()

    def test_is_connected_single_vertex(self):
        g = Graph()
        g.add_vertex(1)
        assert g.is_connected()

    def test_is_connected_directed_true(self):
        # Cycle: 1->2->3->1 is strongly connected
        g = Graph(directed=True)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        assert g.is_connected()

    def test_is_connected_directed_false(self, directed_graph):
        # directed_graph is a DAG — not strongly connected
        assert not directed_graph.is_connected()


# ---------------------------------------------------------------------------
# Display (smoke test — just ensure no exceptions are raised)
# ---------------------------------------------------------------------------

class TestDisplay:
    def test_display_undirected(self, undirected_graph, capsys):
        undirected_graph.display()
        captured = capsys.readouterr()
        assert "Undirected" in captured.out
        assert "Vertices" in captured.out
        assert "Edges" in captured.out

    def test_display_directed(self, directed_graph, capsys):
        directed_graph.display()
        captured = capsys.readouterr()
        assert "Directed" in captured.out
