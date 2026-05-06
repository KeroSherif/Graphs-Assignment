from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List, Optional, TextIO, Tuple


WeightedNeighbor = Tuple[int, int]  # (weight, v)


class Graph:
    """Adjacency-list graph supporting:

    - directed, unweighted edges (topological sort)
    - undirected, weighted edges (Prim's MST)

    Notes:
      - For directed edges, `adj[u]` is `List[int]`.
      - For undirected weighted edges, `adj[u]` is `List[Tuple[int,int]]` as `(weight, v)`.

    Keep graphs separate per algorithm to avoid mixing formats.
    """

    def __init__(self, num_vertices: int):
        if num_vertices < 0:
            raise ValueError("num_vertices must be >= 0")
        self.num_vertices = num_vertices
        self.adj: DefaultDict[int, list] = defaultdict(list)

    def _validate_vertex(self, u: int) -> None:
        if not (0 <= u < self.num_vertices):
            raise ValueError(f"vertex {u} out of range [0, {self.num_vertices - 1}]")

    # --- Edge utilities (Member 1 responsibilities) ---

    def add_directed_edge(self, u: int, v: int) -> None:
        """Add directed unweighted edge u -> v."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        self.adj[u].append(v)

    def add_undirected_weighted_edge(self, u: int, v: int, weight: int) -> None:
        """Add undirected weighted edge u --(weight)-- v."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        self.adj[u].append((weight, v))
        self.adj[v].append((weight, u))

    def add_edge(
        self,
        u: int,
        v: int,
        *,
        directed: bool,
        weight: Optional[int] = None,
    ) -> None:
        """Generic add-edge helper.

        - directed=True expects `weight is None` (topo sort use).
        - directed=False expects `weight is not None` and adds an undirected weighted edge.
        """
        if directed:
            if weight is not None:
                raise ValueError("directed edge should not include weight")
            self.add_directed_edge(u, v)
        else:
            if weight is None:
                raise ValueError("undirected weighted edge requires weight")
            self.add_undirected_weighted_edge(u, v, weight)

    # --- Debugging ---

    def print_graph(self) -> None:
        for u in range(self.num_vertices):
            print(f"{u}: {self.adj[u]}")


@dataclass(frozen=True)
class ParsedGraphInput:
    num_vertices: int
    edges: List[Tuple[int, int, Optional[int]]]


def _strip_comment(line: str) -> str:
    # Allow simple comments in input: everything after '#' is ignored.
    return line.split("#", 1)[0].strip()


def parse_graph_input(
    stream: TextIO,
    *,
    directed: bool,
    weighted: bool,
    one_indexed: bool = False,
) -> ParsedGraphInput:
    """Parse a simple graph input format from a text stream.

    Supported formats (blank lines and `# comments` ignored):

      V
      u v            (directed, unweighted)
      ...

    or

      V
      u v w          (undirected, weighted)
      ...

    You may optionally include an E line after V:

      V
      E
      ...E edge lines...

    If E is provided, parsing stops after E edges.
    """

    raw_lines = [_strip_comment(line) for line in stream.readlines()]
    lines = [ln for ln in raw_lines if ln]

    if not lines:
        raise ValueError("empty input")

    try:
        num_vertices = int(lines[0])
    except ValueError as exc:
        raise ValueError("first non-empty line must be an integer vertex count") from exc

    if num_vertices < 0:
        raise ValueError("vertex count must be >= 0")

    idx = 1
    expected_edges: Optional[int] = None

    if idx < len(lines):
        # If the next line is a single int, treat it as E; else it's the first edge.
        parts = lines[idx].split()
        if len(parts) == 1:
            try:
                expected_edges = int(parts[0])
                if expected_edges < 0:
                    raise ValueError("edge count must be >= 0")
                idx += 1
            except ValueError:
                expected_edges = None

    edges: List[Tuple[int, int, Optional[int]]] = []

    def normalize_vertex(x: int) -> int:
        return x - 1 if one_indexed else x

    while idx < len(lines) and (expected_edges is None or len(edges) < expected_edges):
        parts = lines[idx].split()

        if directed and not weighted:
            if len(parts) != 2:
                raise ValueError(f"expected 'u v' on line {idx + 1}, got: {lines[idx]}")
            u, v = map(int, parts)
            edges.append((normalize_vertex(u), normalize_vertex(v), None))

        elif (not directed) and weighted:
            if len(parts) != 3:
                raise ValueError(f"expected 'u v w' on line {idx + 1}, got: {lines[idx]}")
            u, v, w = map(int, parts)
            edges.append((normalize_vertex(u), normalize_vertex(v), w))

        else:
            raise ValueError("only directed+unweighted or undirected+weighted are supported")

        idx += 1

    if expected_edges is not None and len(edges) != expected_edges:
        raise ValueError(f"expected {expected_edges} edges, found {len(edges)}")

    return ParsedGraphInput(num_vertices=num_vertices, edges=edges)


def build_graph(parsed: ParsedGraphInput, *, directed: bool) -> Graph:
    """Build a Graph from parsed edges."""
    graph = Graph(parsed.num_vertices)
    for u, v, w in parsed.edges:
        graph.add_edge(u, v, directed=directed, weight=w)
    return graph
