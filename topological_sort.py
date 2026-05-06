from __future__ import annotations

from collections import deque
from typing import List

from graph import Graph


def topological_sort(graph: Graph) -> List[int]:
    """Kahn's algorithm (BFS with indegree).

    Member 2: implement here.

    Expected directed graph format:
      graph.adj[u] -> List[int]

    Return: list of vertices in topological order; return [] if a cycle is detected.
    """
    in_degree = [0] * graph.num_vertices
    for u in range(graph.num_vertices):
        for v in graph.adj[u]:
            in_degree[v] += 1

    queue = deque(v for v in range(graph.num_vertices) if in_degree[v] == 0)

    result: List[int] = []
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph.adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(result) != graph.num_vertices:
        return []
    return result


if __name__ == "__main__":
    # Optional quick manual test (Member 2 can replace/remove).
    g = Graph(8)
    edges = [(7, 6), (7, 5), (5, 2), (5, 4), (6, 4), (6, 3), (3, 2), (3, 1), (4, 0), (2, 0), (1, 0)]
    for u, v in edges:
        g.add_directed_edge(u, v)

    print("Topological Order:", topological_sort(g))
