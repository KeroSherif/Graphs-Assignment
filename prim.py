from __future__ import annotations

import heapq
from typing import List, Tuple

from graph import Graph


def prim(graph: Graph, source: int) -> Tuple[List[Tuple[int, int, int]], int]:
    """Prim's MST using a min-heap.

    Member 3: implement here.

    Expected undirected weighted graph format:
      graph.adj[u] -> List[Tuple[int,int]] where (weight, v)

    Return: (mst_edges, total_weight)
      - mst_edges: List of (u, v, weight)
    """
    in_mst = [False] * graph.num_vertices
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0

    # (weight, destination, parent)
    heap: List[Tuple[int, int, int]] = [(0, source, -1)]

    while heap and len(mst_edges) < graph.num_vertices - 1:
      weight, u, parent = heapq.heappop(heap)

      if in_mst[u]:
        continue

      in_mst[u] = True
      if parent != -1:
        mst_edges.append((parent, u, weight))
        total_weight += weight

      for edge_weight, v in graph.adj[u]:
        if not in_mst[v]:
          heapq.heappush(heap, (edge_weight, v, u))

    return mst_edges, total_weight


if __name__ == "__main__":
    # Optional quick manual test (Member 3 can replace/remove).
    g = Graph(9)
    weighted_edges = [
        (0, 1, 4),
        (0, 7, 8),
        (1, 2, 8),
        (1, 7, 11),
        (2, 3, 7),
        (2, 5, 4),
        (2, 8, 2),
        (3, 4, 9),
        (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1),
        (6, 8, 6),
        (7, 8, 7),
    ]
    for u, v, w in weighted_edges:
        g.add_undirected_weighted_edge(u, v, w)

    edges, weight = prim(g, 0)
    print("MST Edges:", edges)
    print("Total Weight:", weight)
